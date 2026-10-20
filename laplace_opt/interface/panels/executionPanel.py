# libraries
from laplace_log import log
from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout,
    QCheckBox, QLineEdit, QPushButton,
    QLabel, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

# project
from ...utils.config_helper import (
    get_from_config, set_in_config
)
from ...utils.model_source import ModelSource


class ExecutionPanel(QGroupBox):
    '''
    Panel handling execution mode and data source configuration.
    
    A lock button allows to enable / disable every widget.
    '''
    # signal indicating that the server checkbox state changed
    server_state_changed = pyqtSignal(bool)

    def __init__(self, source: ModelSource):
        ''' 
        Arg:
            source (ModelSource):
                Object storing the 'model_construction' folder 
                location from which the structure is loaded.
        '''
        super().__init__("Execution & Data Configuration")
        self.source = source
        self.set_up()           # build the elements
        self.actions()          # defines the panel actions


    def set_up(self) -> None:
        '''
        Function made to create and set 
        the elements of the ExecutionPanel.
        '''
        exc_layout = QGridLayout(self)

        # Online execution
        self.server_checkbox = QCheckBox("Start server")
        self.server_entry = QLineEdit("")  # indicates the optimization server address
        self.server_entry.setReadOnly(True)

        # Server port
        self.server_port_entry = QLineEdit()
        self.server_port_entry.setPlaceholderText("Port")
        self.server_port_entry.setFixedWidth(45)
        self.server_port_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Accept only valid TCP/UDP port numbers
        self.server_port_entry.setValidator(QIntValidator(1, 65535, self))

        # Model entry
        self.model_path_entry = QLineEdit()
        self.model_path_entry.setPlaceholderText("model path")
        self.model_browse_button = QPushButton("Model Browse")

        # Saving entry
        self.saving_entry = QLineEdit()
        self.saving_entry.setPlaceholderText("saving path")
        self.save_browse_button = QPushButton("Save Browse")

        # Lock
        self.lock_button = QPushButton("🔒 Lock configuration")
        self.lock_button.setCheckable(True)

        # exc_layout
        exc_layout.addWidget(self.server_checkbox, 0, 0)
        exc_layout.addWidget(QLabel("Server address:"), 0, 1)
        exc_layout.addWidget(self.server_entry, 0, 2)

        exc_layout.addWidget(QLabel("Server port:"), 1, 0)
        exc_layout.addWidget(self.server_port_entry, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        exc_layout.addWidget(QLabel("Model path:"), 1, 1)
        exc_layout.addWidget(self.model_path_entry, 1, 2)
        exc_layout.addWidget(self.model_browse_button, 1, 3)

        exc_layout.addWidget(QLabel("Saving path:"), 2, 1)
        exc_layout.addWidget(self.saving_entry, 2, 2)
        exc_layout.addWidget(self.save_browse_button, 2, 3)

        exc_layout.addWidget(self.lock_button, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)

        exc_layout.setColumnStretch(2, 1) # set the Stretch of the 2nd column, to 1 (other are 0)

        # get the default execution (model and saving) path
            # get and set default saving path
        self.save_path = get_from_config(
            module="interface",
            item="saving_path",
            default_value="",
            type=str
        )
        self.set_path_saving(self.save_path)  # path update when the panel is unlocked
        
            # get and set default model path
        self.set_path_model( str(self.source.root) )

            # Read the port from the configuration
        self.server_port = get_from_config(
            module="server",
            item="port",
            default_value=1254,
            type=int
        )
        self.server_port_entry.setText(str(self.server_port))


    def actions(self) -> None:
        '''
        Defines the actions of the ExecutionPanel class.
        '''
        # when the server checkbox is toggled, emit a PyQt6 signal (to start server)
        self.server_checkbox.toggled.connect(self.update_online_state)
        
        # when the lock_button is pressed, enable / disable the widgets
        self.lock_button.toggled.connect(self.set_locked)

        # when the model button is pressed, select the reading folder
        self.model_browse_button.clicked.connect(
            lambda: self.browse_folder(is_model=True)
        )
        
        # when the save button is pressed, select the saving folder
        self.save_browse_button.clicked.connect(
            lambda: self.browse_folder(is_model=False)
        )

        # when the model path is modified, change the default model path
        self.model_path_entry.textChanged.connect(
            self.on_model_path_changed
        )

        # when the saving path is modified, change the default saving path
        self.saving_entry.textChanged.connect(
            self.on_save_path_changed
        )

        # Update port editability when the server state changes
        self.server_checkbox.toggled.connect(
            self.update_server_port_state
        )

        # Save the port when editing finishes
        self.server_port_entry.editingFinished.connect(
            self.on_server_port_changed
        )


    def on_model_path_changed(self, path: str) -> None:
        '''Change the default model path in 'app_config.ini' '''
        set_in_config(
            module="interface",
            item="model_path",
            val=path,
        )
        log.debug(f"Model folder modified, new model folder: {path}")


    def on_save_path_changed(self, path: str) -> None:
        '''Change the default saving path in 'app_config.ini' '''
        set_in_config(
            module="interface",
            item="saving_path",
            val=path
        )
        log.debug(f"Saving folder modified, new saving folder: {path}")


    def update_online_state(self, checked: bool) -> None:
        '''Change the server state and emit the realted signal.'''
        if not self.lock_button.isChecked():       # if the lock button is not pressed
            self.server_entry.setEnabled(checked)  # enable / disable the server address label
        
        log.debug("Server box checked." if checked else "Server box unchecked.")
        self.server_state_changed.emit(checked)  # emit a signal to start / stop the server


    def set_locked(self, locked: bool) -> None:
        '''
        Enable / disable every widget of the panel 
        when the lock button is clicked.
        '''
        # list of widgets to lock
        widgets = [
            self.server_checkbox,
            self.server_port_entry,
            self.model_path_entry,
            self.model_browse_button,
            self.saving_entry,
            self.save_browse_button,
        ]

        for w in widgets: # for every widget
            w.setEnabled(not locked) # lock / unlock it (locked = True means disable -> Enable = False)

        # change the button text 
        self.lock_button.setText(
            "🔓 Unlock configuration" if locked else "🔒 Lock configuration"
        )
        log.debug("Configuration locked." if locked else "Configuration unlocked.")

        if not locked:  # if unlocking
            if self.get_path_model() != self.model_path:        # if the current model path != the one registered during locked
                self.model_path_entry.setText(self.model_path)  # set the model path
            
            if self.get_path_saving() != self.save_path:   # if the current saving path != the one registered during locked
                self.saving_entry.setText(self.save_path)  # set the saving path 

            self.update_server_port_state(checked=self.is_online_enabled())  # unlock the server port only if server is off


    def browse_folder(self, is_model: bool=True) -> None:
        '''
        Open a QFileDialog to select a folder. Modify the model
        or saving entry according to the button used.
        '''
        path = QFileDialog.getExistingDirectory(
            self,
            "Select folder",
            "",             # initial directory ("" = current working dir)
            QFileDialog.Option.ShowDirsOnly
        )

        # if a folder was selected
        if path:
            # update the corresponding entry
            if is_model:
                self.set_path_model(path)
            else:
                self.set_path_saving(path)


    def update_server_port_state(self, checked: bool = False) -> None:
        '''
        Enable port editing only when the server is off
        and the configuration is unlocked.
        '''
        can_edit = not checked and not self.is_locked()
        self.server_port_entry.setEnabled(can_edit)


    def on_server_port_changed(self) -> None:
        '''Save a valid server port to app_config.ini.'''
        if not self.server_port_entry.hasAcceptableInput():
            self.server_port_entry.setText(str(self.server_port))
            return

        port = int(self.server_port)

        set_in_config(
            module="server",
            item="port",
            val=port
        )

        self.server_port = port
        log.debug(f"Server port modified: {port}")

    ### helpers

    def get_execution(self) -> dict[str, bool | str]:
        '''Return the execution configuration.'''
        execution = {
            "is_online": self.is_online_enabled(),
            "model_path": self.get_path_model(),
            "saving_path": self.get_path_saving(),
            "server_address": self.get_server_address(),
            "server_port": self.get_server_port(),
        }

        return execution

        # checkers
    def is_online_enabled(self) -> bool:
        return self.server_checkbox.isChecked()

    def is_locked(self) -> bool:
        return self.lock_button.isChecked()

        # getters
    def get_path_model(self) -> str:
        return self.model_path_entry.text().strip()

    def get_path_saving(self) -> str:
        return self.saving_entry.text().strip()
    
    def get_server_address(self) -> str:
        return self.server_entry.text().strip()

    def get_server_port(self) -> int:
        '''Return the configured server port.'''
        return int(self.server_port_entry.text())
        
        ### setters
    def set_path_model(self, path: str) -> None:
        if not self.is_locked():
            log.info(f"Model path setted: '{path}'")
            self.model_path_entry.setText(path)
        else:
            log.info(f"Configuration locked, model path unchanged before unlocking.")
        self.model_path = path
    
    def set_path_saving(self, path: str) -> None:
        if not self.is_locked():
            log.info(f"Saving path setted: '{path}'")
            self.saving_entry.setText(path)
        else:
            log.info(f"Configuration locked, saving path unchanged before unlocking.")
        self.save_path = path
    
    def set_server_address(self, address: str) -> None:
        return self.server_entry.setText(address)
