import json
import os
import re
import signal
import sys
import subprocess
import threading
import gettext
import locale

from gi import require_versions
require_versions({"Gtk": "4.0", "Adw": "1"})

from gi.repository import Gtk, Adw, Gio, Gdk, GLib
import locale
import gettext
import llm

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .db_operations import ChatHistory

_ = gettext.gettext

DEBUG = os.environ.get('DEBUG') or False

def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


# Reemplazar la definición de la interfaz D-Bus con XML
DBUS_INTERFACE_XML = """
<node>
  <interface name='org.fuentelibre.gtk_llm_Chat'>
    <method name='OpenConversation'>
      <arg type='s' name='cid' direction='in'/>
    </method>
  </interface>
</node>
"""

class LLMChatApplication(Adw.Application):
    """Class for a chat instance"""

    def __init__(self, config=None):
        super().__init__(
            application_id="org.fuentelibre.gtk_llm_Chat",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )

        self._shutting_down = False  # Bandera para controlar proceso de cierre
        self._window_by_cid = {}  # Mapa de CID -> ventana
        
        debug_print("LLMChatApplication.__init__: Verificando si se necesita configuración inicial...")
        self._needs_initial_setup = self._check_initial_setup_needed()
        debug_print(f"LLMChatApplication.__init__: _needs_initial_setup = {self._needs_initial_setup}")

        # Add signal handler
        signal.signal(signal.SIGINT, self._handle_sigint)
        self.connect('shutdown', self.on_shutdown)  # Conectar señal shutdown



        # Force dark mode until we've tested / liked light mode (issue #25)
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def _handle_sigint(self, signum, frame):
        """Handles SIGINT signal to close the application"""
        debug_print(_("\nClosing application..."))
        self.quit()

    def _register_dbus_interface(self):
        # Solo ejecutar en Linux y evitar timeouts
        if sys.platform != 'linux':
            return
        try:
            from gi.repository import Gio
            # Agregar timeout para evitar bloqueos
            import threading
            
            def register_with_timeout():
                try:
                    connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
                    node_info = Gio.DBusNodeInfo.new_for_xml(DBUS_INTERFACE_XML)
                    interface_info = node_info.interfaces[0]
                    
                    def method_call_handler(connection, sender, object_path, interface_name, method_name, parameters, invocation):
                        if method_name == "OpenConversation":
                            try:
                                cid = parameters.unpack()[0]
                                debug_print(f"D-Bus: Recibida solicitud para abrir conversación CID: '{cid}'")
                                # Usar GLib.idle_add para manejar la llamada en el hilo principal de GTK
                                GLib.idle_add(lambda: self.OpenConversation(cid))
                                invocation.return_value(None)
                            except Exception as e:
                                debug_print(f"D-Bus: Error al procesar OpenConversation: {e}")
                                invocation.return_dbus_error("org.fuentelibre.Error.Failed", str(e))
                        else:
                            invocation.return_error_literal(Gio.DBusError.UNKNOWN_METHOD, "Método desconocido")
                    
                    reg_id = connection.register_object(
                        '/org/fuentelibre/gtk_llm_Chat',
                        interface_info,
                        method_call_handler,
                        None,  # get_property_handler
                        None   # set_property_handler
                    )
                    if reg_id > 0:
                        self.dbus_registration_id = reg_id
                        debug_print("Interfaz D-Bus registrada correctamente")
                    else:
                        debug_print("Error al registrar la interfaz D-Bus")
                except Exception as e:
                    debug_print(f"Error registrando D-Bus: {e}")
            
            # Ejecutar registro en thread separado con timeout
            thread = threading.Thread(target=register_with_timeout, daemon=True)
            thread.start()
            # No esperar - continuar sin D-Bus si hay problemas
            
        except Exception as e:
            debug_print(f"Error al configurar D-Bus (solo debe ocurrir en Linux): {e}")

    def do_startup(self):
        Adw.Application.do_startup(self)
        
        # Configurar recursos básicos de forma segura (solo en hilo principal)
        try:
            # Cargar estilos CSS y configurar tema de iconos en el hilo principal
            from .style_manager import style_manager
            from .resource_manager import resource_manager
            
            # Configurar sin threading para evitar conflictos
            style_manager.load_styles()
            if not resource_manager._icon_theme_configured:
                resource_manager.setup_icon_theme()
            debug_print("Recursos básicos configurados en do_startup")
            
        except Exception as e:
            debug_print(f"Error configurando recursos en startup: {e}")
        
        # Solo registrar D-Bus en Linux
        if sys.platform=='linux':
            self._register_dbus_interface()

        self.hold()  # Asegura que la aplicación no termine prematuramente

        APP_NAME = "gtk-llm-chat"
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(
                    sys._MEIPASS)
        else:
            base_path = os.path.join(os.path.dirname(__file__), "..")

        LOCALE_DIR = os.path.abspath(os.path.join(base_path, 'po'))

        lang = locale.getdefaultlocale()[0]  # Ej: 'es_ES'
        if lang:
            gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
            gettext.textdomain(APP_NAME)
            lang_trans = gettext.translation(APP_NAME, LOCALE_DIR, languages=[lang], fallback=True)
            lang_trans.install()
            global _
            _ = lang_trans.gettext

        self._setup_icon()

        # Configure actions
        rename_action = Gio.SimpleAction.new("rename", None)
        rename_action.connect("activate", self.on_rename_activate)
        self.add_action(rename_action)

        delete_action = Gio.SimpleAction.new("delete", None)
        delete_action.connect("activate", self.on_delete_activate)
        self.add_action(delete_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_activate)
        self.add_action(about_action)

    def OpenConversation(self, cid):
        """Abrir una nueva conversación dado un CID"""
        debug_print(f"D-Bus: OpenConversation recibido con CID: {cid}")
        if not cid:
            debug_print("D-Bus: CID vacío, creando nueva conversación")
            # Siempre crear una nueva ventana cuando el CID está vacío
            self.open_conversation_window({})
            return

        window = self._window_by_cid.get(cid)
        if window is None:
            # Crear y registrar una nueva ventana
            debug_print(f"D-Bus: Creando nueva ventana para CID: {cid}")
            self.open_conversation_window({'cid': cid})
        else:
            # Verificamos si la ventana es válida antes de llamar a present()
            if hasattr(window, 'present') and callable(window.present):
                debug_print(f"D-Bus: Enfocando ventana existente para CID: {cid}")
                window.present()
            else:
                debug_print(f"D-Bus: Error - ventana para CID {cid} no es válida, creando nueva")
                del self._window_by_cid[cid]
                self.open_conversation_window({'cid': cid})

    def create_chat_window(self, cid):
        """Crear una nueva ventana de chat"""
        # Implementación para crear una ventana de chat
        pass

    def on_shutdown(self, app):
        """Handles application shutdown and unregisters D-Bus."""
        self._shutting_down = True
        if hasattr(self, 'dbus_registration_id'):
            connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
            connection.unregister_object(self.dbus_registration_id)

    def get_application_version(self):
        """
        Gets the application version from _version.py.
        """
        try:
            from . import _version
            return _version.__version__
        except ImportError:
            debug_print(_("Error: _version.py not found"))
            return "Unknown"
        return "Unknown"

    def _setup_icon(self):
        """Configures the application icon"""
        # Set search directory
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, 'gtk_llm_chat')
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        icon_theme.add_search_path(base_path)

    def do_command_line(self, command_line):
        """Procesa los argumentos de la línea de comandos."""
        debug_print("do_command_line invocado")

        # Extraer configuración de los argumentos
        args = command_line.get_arguments()
        debug_print(f"Argumentos recibidos: {args}")

        config = {}
        only_applet = False
        legacy_applet = False
        has_args = False  # Flag para saber si se recibieron argumentos relevantes
        
        for arg in args:
            # Skip the executable path (first argument)
            if arg == args[0] and arg.endswith(("gtk-llm-chat", "gtk-llm-chat.exe", "python", "python.exe")):
                continue
                
            has_args = True  # Se recibió al menos un argumento válido
                
            if arg.startswith("--cid="):
                config['cid'] = arg.split("=", 1)[1]
                debug_print(f"CID encontrado en argumentos: {config['cid']}")
            elif arg.startswith("--model="):
                config['model'] = arg.split("=", 1)[1]
            elif arg.startswith("--template="):
                config['template'] = arg.split("=", 1)[1]
            elif arg.startswith("--applet"):
                only_applet = True
            elif arg.startswith("--legacy-applet"):
                legacy_applet = True

        # Guardar esta configuración para usarla
        debug_print(f"Configuración preparada: {config}")

        # Solo proceder con la ventana si no es modo applet
        if not only_applet:
            # Verificar si se necesita mostrar el asistente de configuración inicial
            if self._needs_initial_setup:
                debug_print("Mostrando asistente de configuración inicial desde command_line")
                self._show_welcome_window()
            else:
                # Si no hay argumentos relevantes y la app ya está corriendo, 
                # crear una nueva ventana vacía
                if not has_args and self.get_active_window():
                    debug_print("Aplicación ya en ejecución sin argumentos, creando nueva ventana")
                    self.open_conversation_window({})
                else:
                    self.open_conversation_window(config)
                    
        if legacy_applet:
            self._applet_loaded = True

        return 0

    def _check_initial_setup_needed(self):
        """
        Verifica si se necesita mostrar el asistente de configuración inicial.
        
        Returns:
            bool: True si se necesita mostrar el asistente, False si ya hay configuración
        """
        try:
            # Obtener la ruta de la base de datos usando ensure_user_dir_exists()
            from .platform_utils import ensure_user_dir_exists
            user_dir = ensure_user_dir_exists()
            if not user_dir: # Si ensure_user_dir_exists falla
                debug_print("_check_initial_setup_needed: Error obteniendo user_dir, asumiendo que se necesita setup.")
                return True # Si no podemos obtener el dir, mejor mostrar el welcome.
            user_dir = ensure_user_dir_exists()
            db_path = os.path.join(user_dir, "logs.db")
            
            debug_print(f"_check_initial_setup_needed: user_dir = {user_dir}")
            debug_print(f"_check_initial_setup_needed: db_path = {db_path}")
            debug_print(f"_check_initial_setup_needed: user_dir exists = {os.path.exists(user_dir)}")
            debug_print(f"_check_initial_setup_needed: db_path exists = {os.path.exists(db_path)}")
            
            # Si no existe el archivo logs.db, es la primera vez
            if not os.path.exists(db_path):
                debug_print("_check_initial_setup_needed: Configuración inicial necesaria: logs.db no existe")
                return True
            
            debug_print("_check_initial_setup_needed: Configuración inicial no necesaria: ya existe configuración")
            return False
            
        except Exception as e:
            debug_print(f"_check_initial_setup_needed: Error verificando configuración inicial: {e}")
            # En caso de error, proceder normalmente sin el asistente
            return False

    def do_activate(self):
        """Activa la aplicación y crea una nueva ventana utilizando la configuración actual."""
        Adw.Application.do_activate(self)
        debug_print("do_activate invocado")
        debug_print(f"do_activate: self._needs_initial_setup = {self._needs_initial_setup}")

        # Verificar si se necesita mostrar el asistente de configuración inicial
        if self._needs_initial_setup:
            debug_print("Mostrando asistente de configuración inicial")
            self._show_welcome_window()
        else:
            debug_print("Procediendo con ventana de chat normal")
            self.open_conversation_window()

    def _show_welcome_window(self):
        """Muestra el asistente de configuración inicial."""
        try:
            from .welcome import WelcomeWindow
            
            # Definimos un método que se llamará cuando el usuario termine el asistente
            def on_welcome_finished(config_data=None):
                """Callback que se ejecuta cuando el usuario completa el asistente."""
                debug_print("Asistente de configuración completado")
                
                # Continuar con la apertura de la ventana de chat
                self.open_conversation_window()
            
            welcome_window = WelcomeWindow(self, on_welcome_finished=on_welcome_finished)
            welcome_window.present()
            
        except Exception as e:
            debug_print(f"Error mostrando ventana de bienvenida: {e}")
            # Si hay error con el asistente, proceder con la ventana normal
            self.open_conversation_window()

    def _create_new_window_with_config(self, config):
        """Crea una nueva ventana con la configuración dada."""
        debug_print(f"Creando nueva ventana con configuración: {config}")

        from .chat_window import LLMChatWindow
        from .resource_manager import resource_manager
        chat_history = ChatHistory()

        # Crear la nueva ventana con la configuración
        window = LLMChatWindow(application=self, config=config, chat_history=chat_history)
        resource_manager.set_widget_icon_name(window, "org.fuentelibre.gtk_llm_Chat")

        # Configurar el manejador de eventos de teclado
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_pressed)
        window.add_controller(key_controller)

        # Registrar la ventana por CID si existe
        if 'cid' in config and config['cid']:
            cid = config['cid']
            self._window_by_cid[cid] = window
            debug_print(f"Ventana registrada para CID: {cid}")

        # Presentar la ventana con logs de diagnóstico
        debug_print("Presentando ventana de chat...")
        try:
            window.present()
            debug_print("Ventana de chat presentada correctamente.")
        except Exception as e:
            debug_print(f"[ERROR] Fallo al presentar la ventana: {e}")
        return window

    def _on_key_pressed(self, controller, keyval, keycode, state):
        """Maneja eventos de teclado a nivel de aplicación."""
        window = self.get_active_window()

        # F10: Toggle del sidebar
        if keyval == Gdk.KEY_F10:
            if window and hasattr(window, 'split_view'):
                is_visible = window.split_view.get_show_sidebar()
                window.split_view.set_show_sidebar(not is_visible)
                return True

        # F2: Renombrar conversación
        if keyval == Gdk.KEY_F2:
            if window:
                self.on_rename_activate(None, None)
                return True

        # Escape: Cerrar ventana solo si el input tiene el foco
        if keyval == Gdk.KEY_Escape:
            if window:
                # Verificar si el foco está en el input_text
                if hasattr(window, 'input_text') and window.input_text.has_focus():
                    window.close()
                    return True

        # Permitir que otros controles procesen otros eventos de teclado
        return False

    def on_rename_activate(self, action, param):
        """Renames the current conversation"""
        window = self.get_active_window()
        window.header.set_title_widget(window.title_entry)
        window.title_entry.grab_focus()

    def on_delete_activate(self, action, param):
        """Elimina la conversación actual solo si tiene historial, si no cierra la ventana directamente."""
        window = self.get_active_window()

        # Verificar que tenemos una ventana y acceder a su configuración
        if not window or not hasattr(window, 'config'):
            debug_print("No se puede eliminar: ventana inválida o sin configuración")
            return

        cid = window.config.get('cid')
        chat_history = getattr(window, 'chat_history', None)
        has_history = False
        if cid and chat_history:
            try:
                history_entries = chat_history.get_conversation_history(cid)
                has_history = bool(history_entries)
            except Exception as e:
                debug_print(f"Error consultando historial para CID {cid}: {e}")

        if not has_history:
            debug_print("No hay historial, cerrando ventana directamente (Ctrl+W)")
            window.close()
            return

        # Usar Adw.MessageDialog en vez de Gtk.MessageDialog
        dialog = Adw.MessageDialog(
            transient_for=window,
            modal=True,
            heading=_("Delete Conversation"),
            body=_("Are you sure you want to delete the conversation?")
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("delete", _("Delete"))
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")

        def on_delete_response(dialog, response):
            if response == "delete" and hasattr(window, 'chat_history'):
                cid = window.config.get('cid')
                debug_print(f"Eliminando conversación con CID: {cid}")
                if cid:
                    window.chat_history.delete_conversation(cid)
                    # Cerrar solo la ventana actual en lugar de toda la aplicación
                    window.close()
            dialog.destroy()

        dialog.connect("response", on_delete_response)
        dialog.present()

    def on_about_activate(self, action, param):
        """Shows the 'About' dialog"""
        about_dialog = Adw.AboutWindow(
            transient_for=self.get_active_window(),
            # Keep "Gtk LLM Chat" as the application name
            application_name=_("Gtk LLM Chat"),
            application_icon="org.fuentelibre.gtk_llm_Chat",
            website="https://github.com/icarito/gtk_llm_chat",
            comments=_("A frontend for LLM"),
            license_type=Gtk.License.GPL_3_0,
            developer_name="Sebastian Silva",
            version=self.get_application_version(),
            developers=["Sebastian Silva <sebastian@fuentelibre.org>"],
            copyright="© 2024 Sebastian Silva"
        )
        about_dialog.present()

    def open_conversation_window(self, config=None):
        """
        Abre una ventana de conversación con la configuración dada.

        Args:
            config (dict, optional): Configuración para la ventana de conversación. 
                                    Puede incluir 'cid', 'model', etc.

        Returns:
            LLMChatWindow: La ventana creada o enfocada
        """
        # Asegurar que tenemos una configuración
        config = config or {}

        # Evitar que se abra una ventana de applet
        conversation_config = dict(config)
        if 'applet' in conversation_config:
            conversation_config.pop('applet')

        # Si hay un CID específico en la configuración
        if 'cid' in conversation_config:
            cid = conversation_config['cid']
            debug_print(f"Abriendo ventana con CID específico: {cid}")

            # Verificar si ya existe una ventana registrada para este CID
            if cid in self._window_by_cid:
                window = self._window_by_cid[cid]
                if window.is_visible():
                    debug_print(f"Se encontró ventana registrada para CID {cid}, activándola")
                    window.present()
                    return window
                else:
                    # Si la ventana existe pero no es visible, eliminarla del registro
                    debug_print(f"La ventana para CID {cid} no es visible, eliminando del registro")
                    del self._window_by_cid[cid]

            # Si no existe una ventana para este CID o no es visible, crear una nueva
            debug_print(f"Creando nueva ventana para CID: {cid}")
            return self._create_new_window_with_config(conversation_config)

        else:
            # Si no hay CID específico, crear siempre una nueva ventana de conversación
            debug_print("Creando nueva ventana sin CID específico")
            return self._create_new_window_with_config(conversation_config)
