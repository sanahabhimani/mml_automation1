from automation1.public.controller_configuration import ControllerConfiguration
from automation1.public.controller_files import ControllerFiles
import automation1.internal.capi_error_handler as capi_error_handler
import automation1.internal.capi_wrapper as capi_wrapper
import automation1.internal.c_helpers as c_helpers
import automation1.internal.exception_resolver_gen as exception_resolver
from automation1.public.controller_runtime import ControllerRuntime
import automation1.internal.constants as constants
import ctypes

class Controller():
	'''
	Represents a connection to an Automation1 controller. This is the main class for interacting with an Automation1 controller.
	It has many properties and methods for accessing the features of the Automation1 controller.
	Begin by connecting with the Controller.connect() function and then interact with the returned object.
	'''

	#region Fields

	__constructor_key = object()

	#endregion Fields

	#region Constructor

	def __init__(self, host: str = '::1', username: str = '', password: str = '', expected_certificate = None, constructor_key: object = 0) -> None:
		'''
		Private constructor. You cannot call this, call the Controller.connect() or Controller.connect_secure() function instead.
		'''
		if constructor_key is not Controller.__constructor_key:
			raise PermissionError('Usage of this constructor is not permitted. Use Controller.connect() or Controller.connect_secure() to get a connected Controller object.')

		capi_controller_pointer = ctypes.pointer(ctypes.c_void_p())

		if expected_certificate != None:
			capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_ConnectSecureWithHostAndUser(
			ctypes.create_string_buffer(host.encode('utf-8')),
			ctypes.create_string_buffer(username.encode('utf-8')),
			ctypes.create_string_buffer(password.encode('utf-8')),
			ctypes.create_string_buffer(expected_certificate.encode('utf-8')),
			capi_controller_pointer)
			)
		else:
			capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_ConnectWithHostAndUser(
				ctypes.create_string_buffer(host.encode('utf-8')),
				ctypes.create_string_buffer(username.encode('utf-8')),
				ctypes.create_string_buffer(password.encode('utf-8')),
				capi_controller_pointer)
			)
		self.__capi_controller = capi_controller_pointer.contents
		self.__supported_axis_count = int(capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_AvailableAxisCount(self.__capi_controller)))
		self.__supported_task_count = int(capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_AvailableTaskCount(self.__capi_controller)))
		
		self.__controller_configuration = ControllerConfiguration(self.__capi_controller)
		self.__controller_files = ControllerFiles(self.__capi_controller)
		self.__controller_runtime = ControllerRuntime(self.__capi_controller, self.__supported_axis_count, self.__supported_task_count)

	#endregion Constructor

	#region Properties

	@property
	def is_running(self) -> bool:
		'''
		Gets whether or not the Automation1 controller has started and is currently running (i.e. running AeroScript programs or performing motion).
		If the controller is running you can safely access the controller's runtime components via the "runtime" property.
		'''
		is_running = ctypes.pointer(ctypes.c_bool())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_IsRunning(self.__capi_controller, is_running))
		return is_running.contents.value

	@property
	def name(self) -> str:
		'''
		Gets the name of the connected Automation1 controller.
		'''
		controller_name_max_length = 1024
		controller_name_out = c_helpers.create_c_array(ctypes.c_char, controller_name_max_length)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_Name(self.__capi_controller, controller_name_out, controller_name_max_length))
		return c_helpers.create_py_string_from_c_array(controller_name_out)

	@property
	def serial_number(self) -> str:
		'''
		Gets the serial number of the connected Automation1 controller.
		'''
		controller_serial_number_max_length = 1024
		controller_serial_number_out = c_helpers.create_c_array(ctypes.c_char, controller_serial_number_max_length)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_SerialNumber(self.__capi_controller, controller_serial_number_out, controller_serial_number_max_length))
		return c_helpers.create_py_string_from_c_array(controller_serial_number_out)

	@property
	def is_connection_encrypted(self) -> bool:
		'''
		Gets whether or not the connection with the connected Automation1 Controller is encrypted.
		'''
		is_connection_encrypted = ctypes.pointer(ctypes.c_bool())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_IsConnectionEncrypted(self.__capi_controller, is_connection_encrypted))
		return is_connection_encrypted.contents.value

	@property
	def configuration(self) -> ControllerConfiguration:
		'''
		Gets a way to change the configuration of the Automation1 controller. Configuration is what defines the behavior of the Automation1 controller.
		Changes to configuration usually require a controller reset to take effect.
		'''
		return self.__controller_configuration

	@property
	def files(self) -> ControllerFiles:
		'''
		Gets a way to read and write controller files on the Automation1 controller.
		'''
		return self.__controller_files

	@property
	def runtime(self) -> ControllerRuntime:
		'''
		Gets a way to use the Automation1 controller's runtime components. 
		Accessing this property is only valid if the controller is running.
		You can check the state of the Automation1 controller with the "is_running" property.
		'''
		return self.__controller_runtime

	#endregion Properties

	#region Methods

	@classmethod
	def connect(cls, host: str = '::1', username: str = '', password: str = '') -> 'Controller':
		'''
		Connects to an Automation1 controller running on the specified host with provided username and password.
		Use this method to create and interact with an Automation1 controller.

		Args:
			host: The host name or host IP address of the Automation1 controller to connect to.
			username: The user name for a user with access to the Automation1 controller.
			password: The password for the specified user.

		Returns:
			A new Controller object that represents a connection to the Automation1 controller.
		'''
		return cls(host, username, password, constructor_key=cls.__constructor_key)

	@classmethod
	def connect_usb(cls, username: str = '', password: str = '') -> 'Controller':
		'''
		Connects to an Automation1 drive-based controller that is connected to the same Windows computer over USB.
		Use this method to create and interact with an Automation1 drive-based controller that is connected to 
		the same Windows computer over USB. If access control is enabled on the controller,
		you must specify a user name and password.

		Args:
			username: The user name for a user with access to the drive-based Automation1 controller.
			password: The password for the specified user.

		Returns:
			A new Controller object that represents a connection to the Automation1 controller.
		'''
		return cls.connect(constants.DRIVE_BASED_CONTROLLER_IP_ADDRESS, username, password)

	@classmethod
	def connect_secure(cls, host: str = '::1', username: str = '', password: str = '', expected_certificate = None) -> 'Controller':
		'''
		Connects securely to an Automation1 controller running on the specified host with the provided username and password.
		Use this method to create and interact securely with an Automation1 controller.
		You must specify the controller's certificate because the certificate is used to verify the authenticity of the controller and is used to establish the secure connection.
		See the Automation1 documentation for how to get a controller's certificate.
		If the Automation1 controller's certificate does not match expectedCertificate, a ControllerArgumentException will be thrown.
		To check if communication over your current connection is encrypted, see the "is_connection_encrypted" property.
		Args:
			host: The host name or host IP address of the Automation1 controller to connect to.
			username: The user name for a user with access to the Automation1 controller.
			password: The password for the specified user.
			expected_certificate: The certificate used to verify the authenticity of the Automation1 controller.

		Returns:
			A new Controller object that represents a secure connection to the Automation1 controller.
		'''
		if expected_certificate == None:
			raise exception_resolver.ArgumentException_Connect_TlsExpectedControllerCertificateInvalid()
		return cls(host, username, password, expected_certificate, constructor_key=cls.__constructor_key)

	def disconnect(self):
		'''
		Disconnects from the Automation1 controller.
		Disconnecting will not change the running state of the Automation1 controller (i.e. if it has started and is running, it will remain running).
		After calling this method, this Controller object is no longer usable.
		'''
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Disconnect(self.__capi_controller))

	def start(self):
		'''
		Starts the Automation1 controller if it is not already running.
		Connecting to the Automation1 controller will not change the running state of the controller so use this method to start the controller after connecting.
		If the controller is already running this method does nothing.
		You can check the state of the Automation1 controller with the is_running property.
		'''
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_Start(self.__capi_controller))

	def stop(self):
		'''
		Stops the Automation1 controller if it is currently running.
		If the controller is already stopped this method does nothing.
		You will remain connected to the Automation1 controller after you stop it, 
		stopping the Automation1 controller does not change your connection.
		'''
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_Stop(self.__capi_controller))

	def reset(self):
		'''
		Resets the Automation1 controller, putting the Automation1 controller into a fresh state and performing any initialization.
		The Automation1 controller will be unavailable while the reset is in progress.
		'''
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_Reset(self.__capi_controller))

	def download_mcd_to_file(self, mdk_file_path_to_mcd: str, should_include_files: bool, should_include_configuration: bool):
		'''
		Downloads a machine controller definition (.mcd) file from the controller and saves it to the specified MDK file path. 
		A downloaded machine controller definition file can contain both controller configuration and controller files. 
		This file can be uploaded to any controller to copy this controller's configuration and files.
		When using this function, at least one of the parameters should_include_files and should_include_configuration must be true.

		Args:
			mdk_file_path_to_mcd: The MDK file path to save the downloaded machine controller definition (.mcd) file.
			should_include_files: Whether or not controller files should be included in the download.
			should_include_configuration: Whether or not controller configuration should be included in the download.
		'''
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_DownloadMcdToFile(self.__capi_controller, ctypes.create_string_buffer(mdk_file_path_to_mcd.encode()), should_include_files, should_include_configuration))

	def upload_mcd_to_controller(self, mdk_file_path_to_mcd: str, should_include_files: bool, should_include_configuration: bool, erase_controller: bool):
		'''
		Uploads the machine controller definition (.mcd) file to the controller from the specified MDK file path.
		When using this function, at least of the parameters should_include_files and should_include_configuration must be true.
		Before calling this function, make sure there is nothing important on the controller that could be overwritten 
		or erased. Consider downloading a machine controller definition file as a backup before uploading a different 
		machine controller definition that may overwrite data.

		Args:
			mdk_file_path_to_mcd: The MDK file path of the machine controller definition to upload.
			should_include_files: Whether or not controller files should be included in the upload.
			should_include_configuration: Whether or not controller configuration should be included in the upload.
			erase_controller: Whether or not the controller should be erased before uploading the new files.
		'''
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Controller_UploadMcdToController(self.__capi_controller, ctypes.create_string_buffer(mdk_file_path_to_mcd.encode()), should_include_files, should_include_configuration, erase_controller))

	#endregion Methods
