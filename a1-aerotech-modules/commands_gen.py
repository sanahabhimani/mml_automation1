from automation1.public.enums_gen import *
from automation1.public.status.status_items_gen import *
import automation1.internal.capi_error_handler as capi_error_handler
import automation1.internal.capi_wrapper as capi_wrapper
import automation1.internal.c_helpers as c_helpers
import automation1.internal.argument_checking as argument_checking
import automation1.internal.exception_resolver_gen as exception_resolver
from automation1.internal.axis_input import AxisInput, AxisInputCollection
from automation1.internal.task_input import TaskInput
from automation1.public.command_queue import CommandQueue
from  typing import List, Iterable, Union
import ctypes

class Commands():
	'''
	A class to execute commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor.
		'''
		self.__capi_controller = controller
		self.__device = DeviceCommands(self.__capi_controller)
		self.__advanced_motion = AdvancedMotionCommands(self.__capi_controller)
		self.__servo_loop_tuning = ServoLoopTuningCommands(self.__capi_controller)
		self.__galvo = GalvoCommands(self.__capi_controller)
		self.__fault_and_error = FaultAndErrorCommands(self.__capi_controller)
		self.__motion_setup = MotionSetupCommands(self.__capi_controller)
		self.__safe_zone = SafeZoneCommands(self.__capi_controller)
		self.__transformation = TransformationCommands(self.__capi_controller)
		self.__calibration = CalibrationCommands(self.__capi_controller)
		self.__joystick = JoystickCommands(self.__capi_controller)
		self.__drive_analog_control = DriveAnalogControlCommands(self.__capi_controller)
		self.__autofocus = AutofocusCommands(self.__capi_controller)
		self.__pso = PsoCommands(self.__capi_controller)
		self.__io = IOCommands(self.__capi_controller)
		self.__motion = MotionCommands(self.__capi_controller)

	#endregion Constructor

	#region Properties

	@property
	def device(self) -> 'DeviceCommands':
		'''
		Gets a way to execute Device commands on the Automation1 controller.
		'''
		return self.__device

	@property
	def advanced_motion(self) -> 'AdvancedMotionCommands':
		'''
		Gets a way to execute AdvancedMotion commands on the Automation1 controller.
		'''
		return self.__advanced_motion

	@property
	def servo_loop_tuning(self) -> 'ServoLoopTuningCommands':
		'''
		Gets a way to execute ServoLoopTuning commands on the Automation1 controller.
		'''
		return self.__servo_loop_tuning

	@property
	def galvo(self) -> 'GalvoCommands':
		'''
		Gets a way to execute Galvo commands on the Automation1 controller.
		'''
		return self.__galvo

	@property
	def fault_and_error(self) -> 'FaultAndErrorCommands':
		'''
		Gets a way to execute FaultAndError commands on the Automation1 controller.
		'''
		return self.__fault_and_error

	@property
	def motion_setup(self) -> 'MotionSetupCommands':
		'''
		Gets a way to execute MotionSetup commands on the Automation1 controller.
		'''
		return self.__motion_setup

	@property
	def safe_zone(self) -> 'SafeZoneCommands':
		'''
		Gets a way to execute SafeZone commands on the Automation1 controller.
		'''
		return self.__safe_zone

	@property
	def transformation(self) -> 'TransformationCommands':
		'''
		Gets a way to execute Transformation commands on the Automation1 controller.
		'''
		return self.__transformation

	@property
	def calibration(self) -> 'CalibrationCommands':
		'''
		Gets a way to execute Calibration commands on the Automation1 controller.
		'''
		return self.__calibration

	@property
	def joystick(self) -> 'JoystickCommands':
		'''
		Gets a way to execute Joystick commands on the Automation1 controller.
		'''
		return self.__joystick

	@property
	def drive_analog_control(self) -> 'DriveAnalogControlCommands':
		'''
		Gets a way to execute DriveAnalogControl commands on the Automation1 controller.
		'''
		return self.__drive_analog_control

	@property
	def autofocus(self) -> 'AutofocusCommands':
		'''
		Gets a way to execute Autofocus commands on the Automation1 controller.
		'''
		return self.__autofocus

	@property
	def pso(self) -> 'PsoCommands':
		'''
		Gets a way to execute Pso commands on the Automation1 controller.
		'''
		return self.__pso

	@property
	def io(self) -> 'IOCommands':
		'''
		Gets a way to execute IO commands on the Automation1 controller.
		'''
		return self.__io

	@property
	def motion(self) -> 'MotionCommands':
		'''
		Gets a way to execute Motion commands on the Automation1 controller.
		'''
		return self.__motion

	#endregion Properties

	#region Methods

	def execute(self, aeroscript_text: str, execution_task_index: int = 1) -> None:
		'''
		Executes an AeroScript command on the Automation1 controller on the specified task.

		Args:
			aeroscript_text: The AeroScript string text to compile and execute.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		aeroscript_string = ctypes.create_string_buffer(bytes(aeroscript_text, 'utf-8'))
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_Execute(self.__capi_controller, execution_task_index, aeroscript_string))

	def execute_and_return_aeroscript_axis(self, aeroscript_text: str, execution_task_index: int = 1) -> int:
		'''
		Executes an AeroScript command on the Automation1 controller on the specified task and returns an AeroScript axis value (which is the index of the axis).
		To get a return value from the AeroScript command, set the value of the AeroScript $areturn[0] property in the AeroScript command.
		For example, you could set the aeroscript_text argument to "$areturn[0]=@1" so that this method returns axis index 1 once the AeroScript has finished executing.

		Args:
			aeroscript_text: The AeroScript string text to compile and execute.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the AeroScript $areturn[0] property after the AeroScript command has executed.
		'''
		aeroscript_string = ctypes.create_string_buffer(bytes(aeroscript_text, 'utf-8'))
		aeroscript_axis_index_out = ctypes.pointer(ctypes.c_int32())
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_ExecuteAndReturnAeroScriptAxis(self.__capi_controller, execution_task_index, aeroscript_string, aeroscript_axis_index_out))

		return aeroscript_axis_index_out.contents.value

	def execute_and_return_aeroscript_integer(self, aeroscript_text: str, execution_task_index: int = 1) -> int:
		'''
		Executes an AeroScript command on the Automation1 controller on the specified task and returns an AeroScript integer value.
		To get a return value from the AeroScript command, set the value of the AeroScript $ireturn[0] property in the AeroScript command.
		For example, you could set the aeroscript_text argument to "$ireturn[0]=9999" so that this method returns 9999 once the AeroScript has finished executing.

		Args:
			aeroscript_text: The AeroScript string text to compile and execute.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the AeroScript $ireturn[0] property after the AeroScript command has executed.
		'''
		aeroscript_string = ctypes.create_string_buffer(bytes(aeroscript_text, 'utf-8'))
		aeroscript_integer_out = ctypes.pointer(ctypes.c_int64())
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_ExecuteAndReturnAeroScriptInteger(self.__capi_controller, execution_task_index, aeroscript_string, aeroscript_integer_out))

		return aeroscript_integer_out.contents.value

	def execute_and_return_aeroscript_real(self, aeroscript_text:str, execution_task_index: int = 1) -> float:
		'''
		Executes an AeroScript command on the Automation1 controller on the specified task and returns an AeroScript real value.
		To get a return value from the AeroScript command, set the value of the AeroScript $rreturn[0] property in the AeroScript command.
		For example, you could set the aeroscript_text argument to "$rreturn[0]=0.0001" so that this method returns 0.0001 once the AeroScript has finished executing.

		Args:
			aeroscript_text: The AeroScript string text to compile and execute.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the AeroScript $rreturn[0] property after the AeroScript command has executed.
		'''
		aeroscript_string = ctypes.create_string_buffer(bytes(aeroscript_text, 'utf-8'))
		aeroscript_real_out = ctypes.pointer(ctypes.c_double())
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_ExecuteAndReturnAeroScriptReal(self.__capi_controller, execution_task_index, aeroscript_string, aeroscript_real_out))

		return aeroscript_real_out.contents.value

	def execute_and_return_aeroscript_string(self, aeroscript_text:str, execution_task_index: int = 1) -> str:
		'''
		Executes an AeroScript command on the Automation1 controller on the specified task and returns an AeroScript string value.
		To get a return value from the AeroScript command, set the value of the AeroScript $sreturn[0] property in the AeroScript command.
		For example, you could set the aeroscript_text method argument to "$sreturn[0]=\"HelloWorld\"" so that this method returns "HelloWorld" once the AeroScript has finished executing.

		Args:
			aeroscript_text: The AeroScript string text to compile and execute.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the AeroScript $sreturn[0] property after the AeroScript command has executed.
		'''
		aeroscript_string = ctypes.create_string_buffer(bytes(aeroscript_text, 'utf-8'))
		aeroscript_string_out = c_helpers.create_c_array(ctypes.c_char, 256)
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_ExecuteAndReturnAeroScriptString(self.__capi_controller, execution_task_index, aeroscript_string, aeroscript_string_out, 256))

		return c_helpers.create_py_string_from_c_array(aeroscript_string_out)

	def begin_command_queue(self, task: Union[int, str], command_capacity: int, should_block_if_full: bool) -> CommandQueue:
		'''
		Starts a command queue on the specified task and returns a CommandQueue object to manage and add commands to the new command queue.
		A command queue on a task will store all AeroScript commands added to the command queue and execute them sequentially, in the order they were added.
		Adding AeroScript commands to the command queue does not block (unless the command queue is full and should_block_if_full is True), instead the AeroScript command is added to the command queue and will be executed in the future once all previously added commands are executed.
		A command queue is usually used to avoid the communication latency in between AeroScript commands when executing your motion with the Commands API (such as when using velocity blending where the communication latency will cause deceleration to occur).
		The specified task can only execute queued commands while the command queue is active; non-queued commands from the Commands API and AeroScript programs cannot run while the command queue is active.
		When you are done with the command queue, use the Commands.end_command_queue(CommandQueue) method to end the command queue and return the task to its normal state.

		Args:
			task: The task to create a command queue on.
			command_capacity: The maximum number of unexecuted AeroScript commands that can be stored in the command queue, after which the command queue is full.
				If the number of unexecuted AeroScript commands in the command queue reaches this number, the next AeroScript command added will either block until the command can be added (if should_block_if_full is True) or return produce a ControllerOperationException (if should_block_if_full is False).
			should_block_if_full: Whether or not to block if you add an AeroScript command when the command queue is full. If True, the add will block until the command can be added. If False, a ControllerOperationException will be thrown.

		Returns:
			A CommandQueue object to manage and add commands to the new command queue on the specified task.
		'''
		task_index = TaskInput(task).to_task_index(self.__capi_controller)
		# CTRL-43599: Properly set the task name once CAPI supports converting task indices to names
		if isinstance(task, str):
			task_name = task
		else:
			task_name = ""
		argument_checking.validate_int_32(task_index)
		capi_command_queue_pointer = ctypes.pointer(ctypes.c_void_p())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_CommandQueue_Begin(self.__capi_controller, task_index, command_capacity, should_block_if_full, capi_command_queue_pointer))
		capi_command_queue = capi_command_queue_pointer.contents
		return CommandQueue(self.__capi_controller, capi_command_queue, task_index, task_name, command_capacity, should_block_if_full)

	def end_command_queue(self, command_queue: CommandQueue, milliseconds_timeout: int = -1) -> None:
		'''
		Stops the command queue on the task and returns the task to normal AeroScript execution.
		The currently executing AeroScript command, if any, will be aborted. All remaining queued AeroScript commands will be discarded.
		The specified CommandQueue object is no longer usable after this method is called.

		Args:
			command_queue: The command queue to end.
			milliseconds_timeout: The number of milliseconds to wait to end the command queue. If the command queue takes longer than this amount of time to end, an exception is thrown. This function will wait indefinitely for the command queue to end if this value is set to - 1.
		'''
		if command_queue._capi_command_queue.value == None:
			raise exception_resolver.OperationException_API_CommandQueueEnded()

		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_CommandQueue_End(command_queue._capi_command_queue, milliseconds_timeout))	
		command_queue._capi_command_queue.value = None

	#endregion Methods

class DeviceCommands():
	'''
	A class to execute Device AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def drivearrayread(self, axis: Union[int, str], values_list_to_populate: List[float], start_address: int, num_elements: int, drive_array_type: DriveArrayType) -> None:
		'''
		Reads the contents of the drive array.

		Args:
			axis: The axis from which to read the drive array.
			values_list_to_populate: The list to populate with data that was read from the drive array.
			start_address: Byte-addressable index of the drive array from which to begin reading data.
			num_elements: The number of drive array elements to read.
			drive_array_type: The underlying data type to read from the drive array.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		values_out = c_helpers.create_c_array(ctypes.c_double, num_elements)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(start_address)
		argument_checking.validate_int_64(num_elements)
		argument_checking.validate_int_32(drive_array_type)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveArrayRead(self.__capi_controller, axis, start_address, num_elements, drive_array_type, values_out, num_elements))
		values = c_helpers.create_py_list_from_c_array(values_out, num_elements)
		for i in range(num_elements):
			if i < len(values_list_to_populate):
				values_list_to_populate[i] = values[i]
			else:
				values_list_to_populate.append(values[i])
	
	def drivearraywrite(self, axis: Union[int, str], values_list: List[float], start_address: int, num_elements: int, drive_array_type: DriveArrayType, execution_task_index: int = 1) -> None:
		'''
		Writes the contents of the values_list argument to the drive array.

		This command is deprecated and will be removed in the next major version of Automation1 software. 
		It will be replaced by a command with the same name that does not accept execution_task_index as an argument.

		Args:
			axis: The axis on which to write the drive array.
			values_list: The data to write to the drive array.
			start_address: Byte-addressable index of the drive array at which to begin writing data.
			num_elements: The number of drive array elements to write.
			drive_array_type: The underlying data type to write to the drive array.
			execution_task_index: This argument is unused and will be removed in the next major version of Automation1 software.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(axis)
		values_c_array = c_helpers.create_c_array(ctypes.c_double, values_list)
		argument_checking.validate_int_64(start_address)
		argument_checking.validate_int_64(num_elements)
		argument_checking.validate_int_32(drive_array_type)

		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveArrayWrite(self.__capi_controller, execution_task_index, axis, values_c_array, len(values_list), start_address, num_elements, drive_array_type))

	def drivebrakeoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disengages the brake output and allows the axis to move freely.

		Args:
			axis: The axis on which to disengage the brake.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveBrakeOff(self.__capi_controller, execution_task_index, axis))

	def drivebrakeon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Engages the brake output and prevents the axis from moving freely.

		Args:
			axis: The axis on which to engage the brake.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveBrakeOn(self.__capi_controller, execution_task_index, axis))

	def drivedatacaptureconfigurearray(self, axis: Union[int, str], configuration_number: int, drive_array_start_address: int, number_of_points: int, execution_task_index: int = 1) -> None:
		'''
		Configures the drive array for drive data capture.

		Args:
			axis: The axis on which to configure the drive array for drive data capture.
			configuration_number: The data capture configuration number. When capturing one input signal on the specified axis, specify a value of 0. When capturing two input signals on the specified axis, specify 0 for the first signal and 1 for the second signal.
			drive_array_start_address: The byte-addressable index of the drive array where the first drive data capture value will be written.
			number_of_points: The number of points that will be written to the drive array by drive data capture.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(configuration_number)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_points)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveDataCaptureConfigureArray(self.__capi_controller, execution_task_index, axis, configuration_number, drive_array_start_address, number_of_points))

	def drivedatacaptureconfigureinput(self, axis: Union[int, str], configuration_number: int, input: DriveDataCaptureInput, execution_task_index: int = 1) -> None:
		'''
		Selects the signal that will be stored by drive data capture.

		Args:
			axis: The axis on which to select the drive data capture signal.
			configuration_number: The data capture configuration number. When capturing one input signal on the specified axis, specify a value of 0. When capturing two input signals on the specified axis, specify 0 for the first signal and 1 for the second signal.
			input: The input signal for drive data capture.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(configuration_number)
		argument_checking.validate_int_32(input)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveDataCaptureConfigureInput(self.__capi_controller, execution_task_index, axis, configuration_number, input))

	def drivedatacaptureconfiguretrigger(self, axis: Union[int, str], configuration_number: int, trigger: DriveDataCaptureTrigger, execution_task_index: int = 1) -> None:
		'''
		Selects the event that will trigger drive data capture.

		Args:
			axis: The axis on which to select the drive data capture trigger.
			configuration_number: The data capture configuration number. When capturing one input signal on the specified axis, specify a value of 0. When capturing two input signals on the specified axis, specify 0 for the first signal and 1 for the second signal.
			trigger: The trigger event for drive data capture.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(configuration_number)
		argument_checking.validate_int_32(trigger)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveDataCaptureConfigureTrigger(self.__capi_controller, execution_task_index, axis, configuration_number, trigger))

	def drivedatacaptureoff(self, axis: Union[int, str], configuration_number: int, execution_task_index: int = 1) -> None:
		'''
		Disables drive data capture of configured inputs.

		Args:
			axis: The axis on which to disable drive data capture.
			configuration_number: The data capture configuration number. When capturing one input signal on the specified axis, specify a value of 0. When capturing two input signals on the specified axis, specify 0 for the first signal and 1 for the second signal.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(configuration_number)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveDataCaptureOff(self.__capi_controller, execution_task_index, axis, configuration_number))

	def drivedatacaptureon(self, axis: Union[int, str], configuration_number: int, execution_task_index: int = 1) -> None:
		'''
		Enables drive data capture of configured inputs.

		Args:
			axis: The axis on which to enable drive data capture.
			configuration_number: The data capture configuration number. When capturing one input signal on the specified axis, specify a value of 0. When capturing two input signals on the specified axis, specify 0 for the first signal and 1 for the second signal.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(configuration_number)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveDataCaptureOn(self.__capi_controller, execution_task_index, axis, configuration_number))

	def drivedatacapturereset(self, axis: Union[int, str], configuration_number: int, execution_task_index: int = 1) -> None:
		'''
		Resets drive data capture configuration.

		Args:
			axis: The axis on which to reset drive data capture.
			configuration_number: The data capture configuration number. To reset the first configuration on the specified axis, specify a value of 0. To reset the second configuration on the specified axis, specify a value of 1.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(configuration_number)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveDataCaptureReset(self.__capi_controller, execution_task_index, axis, configuration_number))

	def driveencoderoutputconfiguredirection(self, axis: Union[int, str], output_channel: EncoderOutputChannel, reverse_direction: int, execution_task_index: int = 1) -> None:
		'''
		Inverts the output signal of a specified channel.

		Args:
			axis: The axis on which to apply the configuration.
			output_channel: The outgoing encoder channel.
			reverse_direction: Reverses the direction of the encoder output signal.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(output_channel)
		argument_checking.validate_int_64(reverse_direction)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveEncoderOutputConfigureDirection(self.__capi_controller, execution_task_index, axis, output_channel, reverse_direction))

	def driveencoderoutputconfiguredivider(self, axis: Union[int, str], output_channel: EncoderOutputChannel, output_divider: int, execution_task_index: int = 1) -> None:
		'''
		Applies a divider on the specified output channel, lowering the frequency of output signals.

		Args:
			axis: The axis on which to apply the configuration.
			output_channel: The outgoing encoder channel.
			output_divider: The divider to apply to encoder output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(output_channel)
		argument_checking.validate_int_64(output_divider)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveEncoderOutputConfigureDivider(self.__capi_controller, execution_task_index, axis, output_channel, output_divider))

	def driveencoderoutputconfigureinput(self, axis: Union[int, str], output_channel: EncoderOutputChannel, input_channel: EncoderInputChannel, execution_task_index: int = 1) -> None:
		'''
		Configures an output channel to echo encoder signals from the specified input channel.

		Args:
			axis: The axis on which to apply the configuration.
			output_channel: The outgoing encoder channel.
			input_channel: The incoming encoder channel.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(output_channel)
		argument_checking.validate_int_32(input_channel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveEncoderOutputConfigureInput(self.__capi_controller, execution_task_index, axis, output_channel, input_channel))

	def driveencoderoutputoff(self, axis: Union[int, str], output_channel: EncoderOutputChannel, execution_task_index: int = 1) -> None:
		'''
		Disables encoder output on the specified output channel.

		Args:
			axis: The axis on which to disable encoder output.
			output_channel: The outgoing encoder channel.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(output_channel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveEncoderOutputOff(self.__capi_controller, execution_task_index, axis, output_channel))

	def driveencoderoutputon(self, axis: Union[int, str], output_channel: EncoderOutputChannel, output_mode: EncoderOutputMode, execution_task_index: int = 1) -> None:
		'''
		Enables encoder output on the specified output channel.

		Args:
			axis: The axis on which to enable encoder output.
			output_channel: The outgoing encoder channel.
			output_mode: This argument is unused and will be removed in the next major version of Automation1 software. You must specify EncoderOutputMode.Default.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(output_channel)
		argument_checking.validate_int_32(output_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveEncoderOutputOn(self.__capi_controller, execution_task_index, axis, output_channel, output_mode))

	def drivegetitem(self, axis: Union[int, str], drive_item: DriveItem, additional_data: int, execution_task_index: int = 1) -> float:
		'''
		Gets the specified drive item from the specified axis.

		Args:
			axis: The axis from which to retrieve the drive item value.
			drive_item: The drive item to retrieve.
			additional_data: Additional data for the specified drive item. This argument is required by some drive items.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified drive item.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(drive_item)
		argument_checking.validate_int_64(additional_data)
		returnOut = ctypes.pointer(ctypes.c_double())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveGetItem(self.__capi_controller, execution_task_index, axis, drive_item, additional_data, returnOut))
		return returnOut.contents.value

	def drivepulsestreamconfigure(self, output_axis: Union[int, str], input_axes: Union[int, str, Iterable[Union[int, str]]], input_scale_factors: List[float], execution_task_index: int = 1) -> None:
		'''
		Configures pulse streaming mode.

		Args:
			output_axis: The output axis on which to configure pulse streaming mode.
			input_axes: A list of one or more axes which will be tracked.
			input_scale_factors: A list of scale factors to apply to each axis in the $inputAxes array.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		output_axis = AxisInput(output_axis).to_axis_index(self.__capi_controller)
		input_axes = AxisInputCollection(input_axes).to_axis_indices(self.__capi_controller)
		input_axes_c_array = c_helpers.create_c_array(ctypes.c_int32, input_axes)
		input_scale_factors_c_array = c_helpers.create_c_array(ctypes.c_double, input_scale_factors)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(output_axis)
		argument_checking.validate_int_32(input_axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DrivePulseStreamConfigure(self.__capi_controller, execution_task_index, output_axis, input_axes_c_array, len(input_axes), input_scale_factors_c_array, len(input_scale_factors)))

	def drivepulsestreamconfigurewithsignalmode(self, output_axis: Union[int, str], input_axes: Union[int, str, Iterable[Union[int, str]]], input_scale_factors: List[float], signal_mode: DrivePulseStreamSignalMode, execution_task_index: int = 1) -> None:
		'''
		Configures pulse streaming mode.

		Args:
			output_axis: The output axis on which to configure pulse streaming mode.
			input_axes: A list of one or more axes which will be tracked.
			input_scale_factors: A list of scale factors to apply to each axis in the $inputAxes array.
			signal_mode: The signal mode used when DriveEncoderOutputConfigureInput() and DriveEncoderOutputOn() are configured to echo the Pulse Stream signal to an encoder output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		output_axis = AxisInput(output_axis).to_axis_index(self.__capi_controller)
		input_axes = AxisInputCollection(input_axes).to_axis_indices(self.__capi_controller)
		input_axes_c_array = c_helpers.create_c_array(ctypes.c_int32, input_axes)
		input_scale_factors_c_array = c_helpers.create_c_array(ctypes.c_double, input_scale_factors)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(output_axis)
		argument_checking.validate_int_32(input_axes)
		argument_checking.validate_int_32(signal_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DrivePulseStreamConfigureWithSignalMode(self.__capi_controller, execution_task_index, output_axis, input_axes_c_array, len(input_axes), input_scale_factors_c_array, len(input_scale_factors), signal_mode))

	def drivepulsestreamoff(self, output_axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables pulse streaming mode on an axis.

		Args:
			output_axis: The axis on which to disable pulse streaming mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		output_axis = AxisInput(output_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(output_axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DrivePulseStreamOff(self.__capi_controller, execution_task_index, output_axis))

	def drivepulsestreamon(self, output_axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables pulse streaming mode on an axis.

		Args:
			output_axis: The axis on which to enable pulse streaming mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		output_axis = AxisInput(output_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(output_axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DrivePulseStreamOn(self.__capi_controller, execution_task_index, output_axis))

	def drivesetauxiliaryfeedback(self, axis: Union[int, str], auxiliary_feedback: float, execution_task_index: int = 1) -> None:
		'''
		Sets the auxiliary feedback of the axis.

		Args:
			axis: The axis on which to set the auxiliary feedback.
			auxiliary_feedback: The feedback value to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		
		This command is deprecated and will be removed in the next major version of Automation1 software. This function has been obsoleted by DriveSetEncoderPosition(). Use that function instead to set the auxiliary feedback.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveSetAuxiliaryFeedback(self.__capi_controller, execution_task_index, axis, auxiliary_feedback))

	def drivesetencoderposition(self, axis: Union[int, str], encoder_channel: DriveEncoderChannel, encoder_value: float, execution_task_index: int = 1) -> None:
		'''
		Sets the hardware position counter of a drive encoder.

		Args:
			axis: The axis on which to set the hardware position counter of a drive encoder.
			encoder_channel: The drive encoder on which to set the hardware position counter.
			encoder_value: The value to set to the hardware position counter.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(encoder_channel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveSetEncoderPosition(self.__capi_controller, execution_task_index, axis, encoder_channel, encoder_value))

	def drivesetpositioncommand(self, axis: Union[int, str], position_command_value: float, execution_task_index: int = 1) -> None:
		'''
		Sets the position command value of the specified axis at the servo loop level and adjusts the position feedback for position error.

		Args:
			axis: The axis on which to set the position command.
			position_command_value: The position command value to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveSetPositionCommand(self.__capi_controller, execution_task_index, axis, position_command_value))

	def drivesetpositionfeedback(self, axis: Union[int, str], position_feedback_value: float, execution_task_index: int = 1) -> None:
		'''
		Sets the position command and the position feedback value of the specified axis at the servo loop level.

		Args:
			axis: The axis on which to set the position command.
			position_feedback_value: The position feedback value to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveSetPositionFeedback(self.__capi_controller, execution_task_index, axis, position_feedback_value))

	#endregion Methods

class AdvancedMotionCommands():
	'''
	A class to execute AdvancedMotion AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def cammingfreetable(self, table_num: int, execution_task_index: int = 1) -> None:
		'''
		Unloads a camming table from the SMC.

		Args:
			table_num: The camming table number to remove. This value must be greater than or equal to 0 and less than or equal to 99.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(table_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CammingFreeTable(self.__capi_controller, execution_task_index, table_num))

	def cammingloadtablefromarray(self, table_num: int, leader_values: List[float], follower_values: List[float], num_values: int, units_mode: CammingUnits, interpolation_mode: CammingInterpolation, wrap_mode: CammingWrapping, table_offset: float, execution_task_index: int = 1) -> None:
		'''
		Loads a camming table into the SMC.

		Args:
			table_num: The camming table number to use. This value must be greater than or equal to 0 and less than or equal to 99. Use this number when using the CammingOn() and CammingFreeTable() functions.
			leader_values: Array of leader axis position values for the follower axis to track.
			follower_values: Array of follower axis positions or velocities to use.
			num_values: The number of values in the leaderValues and followerValues arrays.
			units_mode: The units of the values in the camming table.
			interpolation_mode: The interpolation type to use if the position of the leader axis is between two values in the table.
			wrap_mode: Determines how a leader axis position value outside of the table is treated.
			table_offset: An offset applied to all follower axis position or velocity values in the table.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		leader_values_c_array = c_helpers.create_c_array(ctypes.c_double, leader_values)
		follower_values_c_array = c_helpers.create_c_array(ctypes.c_double, follower_values)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(table_num)
		argument_checking.validate_int_64(num_values)
		argument_checking.validate_int_32(units_mode)
		argument_checking.validate_int_32(interpolation_mode)
		argument_checking.validate_int_32(wrap_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CammingLoadTableFromArray(self.__capi_controller, execution_task_index, table_num, leader_values_c_array, len(leader_values), follower_values_c_array, len(follower_values), num_values, units_mode, interpolation_mode, wrap_mode, table_offset))

	def cammingoff(self, follower_axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables camming on the specified follower axis.

		Args:
			follower_axis: The follower axis on which to disable camming.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		follower_axis = AxisInput(follower_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(follower_axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CammingOff(self.__capi_controller, execution_task_index, follower_axis))

	def cammingon(self, follower_axis: Union[int, str], leader_axis: Union[int, str], table_num: int, source: CammingSource, output: CammingOutput, execution_task_index: int = 1) -> None:
		'''
		Enables camming on the specified leader axis and follower axis.

		Args:
			follower_axis: The axis to set as the follower axis.
			leader_axis: The axis to set as the leader axis.
			table_num: The camming table number to use. This value must be greater than or equal to 0 and less than or equal to 99.
			source: The signal on the leader axis that the follower axis will track.
			output: The output signal to generate and the synchronization mode to use on the camming follower axis.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		follower_axis = AxisInput(follower_axis).to_axis_index(self.__capi_controller)
		leader_axis = AxisInput(leader_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(follower_axis)
		argument_checking.validate_int_32(leader_axis)
		argument_checking.validate_int_64(table_num)
		argument_checking.validate_int_32(source)
		argument_checking.validate_int_32(output)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CammingOn(self.__capi_controller, execution_task_index, follower_axis, leader_axis, table_num, source, output))

	def gearingoff(self, follower_axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables gearing on an axis.

		Args:
			follower_axis: The axis on which to disable gearing.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		follower_axis = AxisInput(follower_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(follower_axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GearingOff(self.__capi_controller, execution_task_index, follower_axis))

	def gearingon(self, follower_axis: Union[int, str], filter: GearingFilter, execution_task_index: int = 1) -> None:
		'''
		Enables gearing on an axis.

		Args:
			follower_axis: The axis on which to enable gearing.
			filter: Type of filter applied to follower axis motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		follower_axis = AxisInput(follower_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(follower_axis)
		argument_checking.validate_int_32(filter)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GearingOn(self.__capi_controller, execution_task_index, follower_axis, filter))

	def gearingsetleaderaxis(self, follower_axis: Union[int, str], leader_axis: Union[int, str], gearing_source: GearingSource, execution_task_index: int = 1) -> None:
		'''
		Configures gearing for an axis.

		Args:
			follower_axis: Follower axis for the gearing setup.
			leader_axis: Leader axis for the gearing setup.
			gearing_source: Input data source for gearing.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		follower_axis = AxisInput(follower_axis).to_axis_index(self.__capi_controller)
		leader_axis = AxisInput(leader_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(follower_axis)
		argument_checking.validate_int_32(leader_axis)
		argument_checking.validate_int_32(gearing_source)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GearingSetLeaderAxis(self.__capi_controller, execution_task_index, follower_axis, leader_axis, gearing_source))

	def gearingsetratio(self, follower_axis: Union[int, str], gear_ratio: float, execution_task_index: int = 1) -> None:
		'''
		Sets the gearing ratio for an axis.

		Args:
			follower_axis: The axis on which to set the gear ratio.
			gear_ratio: The scale factor applied to the motion of the follower axis, specified as the ratio of follower axis counts to leader axis counts. A negative gear ratio will cause the follower axis to move in the opposite direction of the motion of the leader axis.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		follower_axis = AxisInput(follower_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(follower_axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GearingSetRatio(self.__capi_controller, execution_task_index, follower_axis, gear_ratio))

	def moveoutoflimit(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Executes an asynchronous move on an axis to move it out of a limit condition.

		Args:
			axis: The axis on which to perform the move.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveOutOfLimit(self.__capi_controller, execution_task_index, axis))

	def movetolimitccw(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Executes an asynchronous move on an axis to move it into a limit condition in the counterclockwise direction.

		Args:
			axis: The axis on which to perform the move.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveToLimitCcw(self.__capi_controller, execution_task_index, axis))

	def movetolimitcw(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Executes an asynchronous move on an axis to move it into a limit condition in the clockwise direction.

		Args:
			axis: The axis on which to perform the move.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveToLimitCw(self.__capi_controller, execution_task_index, axis))

	def normalcyoff(self, execution_task_index: int = 1) -> None:
		'''
		Disables normalcy mode.

		Args:
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_NormalcyOff(self.__capi_controller, execution_task_index))

	def normalcyon(self, normalcy_alignment: NormalcyAlignment, execution_task_index: int = 1) -> None:
		'''
		Enables normalcy mode.

		Args:
			normalcy_alignment: The type of the normalcy mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(normalcy_alignment)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_NormalcyOn(self.__capi_controller, execution_task_index, normalcy_alignment))

	def normalcysetaxes(self, normalcy_axis: Union[int, str], plane_axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Configures the axes to use for normalcy mode.

		Args:
			normalcy_axis: The normalcy axis. This must be a dependent type axis.
			plane_axes: The axes to use as the X and Y axes of the normalcy plane. These axes must be dominant type axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		normalcy_axis = AxisInput(normalcy_axis).to_axis_index(self.__capi_controller)
		plane_axes = AxisInputCollection(plane_axes).to_axis_indices(self.__capi_controller)
		plane_axes_c_array = c_helpers.create_c_array(ctypes.c_int32, plane_axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(normalcy_axis)
		argument_checking.validate_int_32(plane_axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_NormalcySetAxes(self.__capi_controller, execution_task_index, normalcy_axis, plane_axes_c_array, len(plane_axes)))

	def normalcysettolerance(self, tolerance: float, execution_task_index: int = 1) -> None:
		'''
		Configures the tolerance to use for normalcy mode.

		Args:
			tolerance: The normalcy mode tolerance, in degrees.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_NormalcySetTolerance(self.__capi_controller, execution_task_index, tolerance))

	#endregion Methods

class ServoLoopTuningCommands():
	'''
	A class to execute ServoLoopTuning AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def tuningsetfeedforwardgains(self, axis: Union[int, str], feedforward_gains: List[FeedforwardGain], feedforward_gain_values: List[float], execution_task_index: int = 1) -> None:
		'''
		Sets the specified feedforward gain values on the specified axis.

		Args:
			axis: The axis on which to set the gain values.
			feedforward_gains: A list of feedforward gains to set.
			feedforward_gain_values: A list of feedforward gain values to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		feedforward_gains_c_array = c_helpers.create_c_array(ctypes.c_int32, feedforward_gains)
		feedforward_gain_values_c_array = c_helpers.create_c_array(ctypes.c_double, feedforward_gain_values)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(feedforward_gains)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TuningSetFeedforwardGains(self.__capi_controller, execution_task_index, axis, feedforward_gains_c_array, len(feedforward_gains), feedforward_gain_values_c_array, len(feedforward_gain_values)))

	def tuningsetmotorangle(self, axis: Union[int, str], current: float, angle: float, execution_task_index: int = 1) -> None:
		'''
		Generates an open-loop current command at a fixed electrical angle.

		Args:
			axis: The axis on which to command current.
			current: The current to output, specified in amperes.
			angle: The electrical angle, specified in degrees. 360 degrees is one electrical commutation cycle of the motor.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TuningSetMotorAngle(self.__capi_controller, execution_task_index, axis, current, angle))

	def tuningsetmotorcurrent(self, axis: Union[int, str], current: float, duration: int, execution_task_index: int = 1) -> None:
		'''
		Generates an open-loop current command at a rotating electrical angle.

		Args:
			axis: The axis on which to command current.
			current: The current to output, specified in amperes.
			duration: The amount of time to output current, specified in milliseconds. Specify 0 to output current continuously.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(duration)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TuningSetMotorCurrent(self.__capi_controller, execution_task_index, axis, current, duration))

	def tuningsetservoloopgains(self, axis: Union[int, str], servo_gains: List[ServoLoopGain], servo_gain_values: List[float], execution_task_index: int = 1) -> None:
		'''
		Sets the specified servo loop gain values on the specified axis.

		Args:
			axis: The axis on which to set the gain values.
			servo_gains: A list of servo loop gains to set.
			servo_gain_values: A list of servo loop gain values to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		servo_gains_c_array = c_helpers.create_c_array(ctypes.c_int32, servo_gains)
		servo_gain_values_c_array = c_helpers.create_c_array(ctypes.c_double, servo_gain_values)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(servo_gains)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TuningSetServoLoopGains(self.__capi_controller, execution_task_index, axis, servo_gains_c_array, len(servo_gains), servo_gain_values_c_array, len(servo_gain_values)))

	#endregion Methods

class GalvoCommands():
	'''
	A class to execute Galvo AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def galvoconfigurelaser1pulsewidth(self, axis: Union[int, str], time: float, execution_task_index: int = 1) -> None:
		'''
		Specifies the pulse width, in microseconds, of the O1 signal.

		Args:
			axis: The axis on which to configure the laser 1 pulse width.
			time: The time value in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureLaser1PulseWidth(self.__capi_controller, execution_task_index, axis, time))

	def galvoconfigurelaser2pulsewidth(self, axis: Union[int, str], time: float, execution_task_index: int = 1) -> None:
		'''
		Specifies the pulse width, in microseconds, of the O2 signal.

		Args:
			axis: The axis on which to configure the laser 2 pulse width.
			time: The time value in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureLaser2PulseWidth(self.__capi_controller, execution_task_index, axis, time))

	def galvoconfigurelaserdelays(self, axis: Union[int, str], on_delay: float, off_delay: float, execution_task_index: int = 1) -> None:
		'''
		Specifies when the axis fires the laser relative to when you command the laser to power on and when the axis stops firing the laser relative to when you command the laser to power off.

		Args:
			axis: The axis on which to configure laser delays.
			on_delay: The delay time, in microseconds, that is necessary for the laser to power on. If your program uses the automatic laser mode, this value must be greater than or equal to -32,768 and less than or equal to 32,767. If your program uses the manual laser mode or if you are operating in IFOV mode, this value must be greater than or equal to -975 and less than or equal to 32,767.
			off_delay: The delay time, in microseconds, that is necessary for the laser to power off. This value must be greater than or equal to -975 and less than or equal to 2,000,000.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureLaserDelays(self.__capi_controller, execution_task_index, axis, on_delay, off_delay))

	def galvoconfigurelasermode(self, axis: Union[int, str], laser_mode: int, execution_task_index: int = 1) -> None:
		'''
		Specifies the mode in which the laser output signals operate.

		Args:
			axis: The axis on which to configure the laser mode.
			laser_mode: The value of the laser output mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(laser_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureLaserMode(self.__capi_controller, execution_task_index, axis, laser_mode))

	def galvoconfigurelaseroutputperiod(self, axis: Union[int, str], time: float, execution_task_index: int = 1) -> None:
		'''
		Specifies the period, in microseconds, of the O1 and O2 signals.

		Args:
			axis: The axis on which to configure the laser output period.
			time: The time value in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureLaserOutputPeriod(self.__capi_controller, execution_task_index, axis, time))

	def galvoconfigurestandbyperiod(self, axis: Union[int, str], time: float, execution_task_index: int = 1) -> None:
		'''
		Specifies the period, in microseconds, of the standby signals.

		Args:
			axis: The axis on which to configure the standby period.
			time: The time value in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureStandbyPeriod(self.__capi_controller, execution_task_index, axis, time))

	def galvoconfigurestandbypulsewidth(self, axis: Union[int, str], time: float, execution_task_index: int = 1) -> None:
		'''
		Specifies the pulse width, in microseconds, of the standby signals.

		Args:
			axis: The axis on which to configure the standby pulse width.
			time: The time value in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureStandbyPulseWidth(self.__capi_controller, execution_task_index, axis, time))

	def galvoconfiguresuppressionpulsewidth(self, axis: Union[int, str], time: float, execution_task_index: int = 1) -> None:
		'''
		Specifies the pulse width, in microseconds, of the suppression signal.

		Args:
			axis: The axis on which to configure the suppression pulse width.
			time: The time value in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoConfigureSuppressionPulseWidth(self.__capi_controller, execution_task_index, axis, time))

	def galvoencoderscalefactorset(self, axis: Union[int, str], encoder_scale_factor: float, execution_task_index: int = 1) -> None:
		'''
		Enables "marking on the fly" functionality.

		Args:
			axis: The axis on which to configure the encoder scale factor.
			encoder_scale_factor: The ratio of scanner counts to encoder counts. This value must be greater than -32,768 and less than 32,767.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoEncoderScaleFactorSet(self.__capi_controller, execution_task_index, axis, encoder_scale_factor))

	def galvolaseroutput(self, axis: Union[int, str], laser_state: GalvoLaser, execution_task_index: int = 1) -> None:
		'''
		Specifies how the laser on a galvo axis is controlled.

		Args:
			axis: The axis on which to configure the laser state.
			laser_state: The mode to use to control the laser.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(laser_state)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoLaserOutput(self.__capi_controller, execution_task_index, axis, laser_state))

	def galvoprojectionoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the projective transformation on galvo axes.

		Args:
			axis: The galvo axis on which to disable the projection.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoProjectionOff(self.__capi_controller, execution_task_index, axis))

	def galvoprojectionon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the projective transformation on galvo axes.

		Args:
			axis: The galvo axis on which to apply the projection.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoProjectionOn(self.__capi_controller, execution_task_index, axis))

	def galvoprojectionsetcoefficients(self, axis: Union[int, str], coefficients: List[float], execution_task_index: int = 1) -> None:
		'''
		Specifies the projective transformation coefficients that are applied to galvo axes.

		Args:
			axis: The galvo axis on which the projection is to be applied.
			coefficients: The coefficients to use.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		coefficients_c_array = c_helpers.create_c_array(ctypes.c_double, coefficients)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoProjectionSetCoefficients(self.__capi_controller, execution_task_index, axis, coefficients_c_array, len(coefficients)))

	def galvorotationset(self, axis: Union[int, str], angle: float, execution_task_index: int = 1) -> None:
		'''
		Specifies an angle of rotation that is applied to galvo axes.

		Args:
			axis: The galvo axis on which the rotation is to be applied.
			angle: The angle in degrees.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoRotationSet(self.__capi_controller, execution_task_index, axis, angle))

	def galvowobbleoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the galvo wobble feature.

		Args:
			axis: The galvo axis on which the galvo wobble is to be disabled.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoWobbleOff(self.__capi_controller, execution_task_index, axis))

	def galvowobbleon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the galvo wobble feature.

		Args:
			axis: The galvo axis on which the galvo wobble is to be applied.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoWobbleOn(self.__capi_controller, execution_task_index, axis))

	def galvowobblesetconfiguration(self, axis: Union[int, str], amplitude_parallel: float, amplitude_perpendicular: float, frequency: float, wobble_mode: GalvoWobbleMode, wobble_type: GalvoWobbleType, execution_task_index: int = 1) -> None:
		'''
		Configures the wobble feature, which generates a wobble pattern that is added to the motion command of a galvo axis.

		Args:
			axis: The galvo axis on which the galvo wobble is to be applied.
			amplitude_parallel: The amplitude of the wobble shape parallel to the vector path.
			amplitude_perpendicular: The amplitude of the wobble shape perpendicular to the vector path.
			frequency: The frequency of the wobble oscillation. Specified in hertz for time-based mode or user units for distance-based mode.
			wobble_mode: Specifies whether the wobble is repeated based on a fixed time or a fixed vector distance.
			wobble_type: The type of figure that is generated by the wobble.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(wobble_mode)
		argument_checking.validate_int_32(wobble_type)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_GalvoWobbleSetConfiguration(self.__capi_controller, execution_task_index, axis, amplitude_parallel, amplitude_perpendicular, frequency, wobble_mode, wobble_type))

	def ifovoff(self, execution_task_index: int = 1) -> None:
		'''
		Disables Infinite Field of View (IFOV).

		Args:
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovOff(self.__capi_controller, execution_task_index))

	def ifovon(self, execution_task_index: int = 1) -> None:
		'''
		Enables Infinite Field of View (IFOV).

		Args:
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovOn(self.__capi_controller, execution_task_index))

	def ifovsetaxispairs(self, axis_pair_h: Union[int, str, Iterable[Union[int, str]]], axis_pair_v: Union[int, str, Iterable[Union[int, str]]], scale_factor_h: float, scale_factor_v: float, execution_task_index: int = 1) -> None:
		'''
		Configures axes to command in Infinite Field of View (IFOV).

		Args:
			axis_pair_h: The horizontal axis pair. This pair consists of a galvo axis and its corresponding servo axis.
			axis_pair_v: The vertical axis pair. This pair consists of a galvo axis and its corresponding servo axis.
			scale_factor_h: Specifies the scaling from the servo axis to the galvo axis in the horizontal axis pair.
			scale_factor_v: Specifies the scaling from the servo axis to the galvo axis in the vertical axis pair.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis_pair_h = AxisInputCollection(axis_pair_h).to_axis_indices(self.__capi_controller)
		axis_pair_v = AxisInputCollection(axis_pair_v).to_axis_indices(self.__capi_controller)
		axis_pair_h_c_array = c_helpers.create_c_array(ctypes.c_int32, axis_pair_h)
		axis_pair_v_c_array = c_helpers.create_c_array(ctypes.c_int32, axis_pair_v)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis_pair_h)
		argument_checking.validate_int_32(axis_pair_v)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovSetAxisPairs(self.__capi_controller, execution_task_index, axis_pair_h_c_array, len(axis_pair_h), axis_pair_v_c_array, len(axis_pair_v), scale_factor_h, scale_factor_v))

	def ifovsetsize(self, size: float, execution_task_index: int = 1) -> None:
		'''
		Configures the field of view size of the galvo head in Infinite Field of View (IFOV).

		Args:
			size: The field of view size, in user units, of the galvo head.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovSetSize(self.__capi_controller, execution_task_index, size))

	def ifovsetsyncaxes(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Configures more axes to command in Infinite Field of View (IFOV).

		Args:
			axes: A list of axes to synchronize in Infinite Field of View in addition to those specified in IfovSetAxisPairs().
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovSetSyncAxes(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def ifovsettime(self, time: int, execution_task_index: int = 1) -> None:
		'''
		Configures the maximum search time that the controller looks ahead in Infinite Field of View (IFOV).

		Args:
			time: The time, in milliseconds, that the controller looks ahead.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(time)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovSetTime(self.__capi_controller, execution_task_index, time))

	def ifovsettrackingacceleration(self, acceleration: float, execution_task_index: int = 1) -> None:
		'''
		Configures the maximum acceleration of the servo axes while in Infinite Field of View (IFOV).

		Args:
			acceleration: The maximum acceleration, in user units/second squared, of the servo axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovSetTrackingAcceleration(self.__capi_controller, execution_task_index, acceleration))

	def ifovsettrackingspeed(self, speed: float, execution_task_index: int = 1) -> None:
		'''
		Configures the maximum speed of the servo axes while in Infinite Field of View (IFOV).

		Args:
			speed: The maximum speed, in user units/time base, of the servo axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_IfovSetTrackingSpeed(self.__capi_controller, execution_task_index, speed))

	#endregion Methods

class FaultAndErrorCommands():
	'''
	A class to execute FaultAndError AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def acknowledgeall(self, execution_task_index: int = 1) -> None:
		'''
		Acknowledges all axis faults and clears all task errors.

		Args:
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AcknowledgeAll(self.__capi_controller, execution_task_index))

	def faultacknowledge(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Acknowledges faults on axes.

		Args:
			axes: The axes on which to acknowledge faults.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_FaultAcknowledge(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def faultthrow(self, axis: Union[int, str], fault_mask: int, execution_task_index: int = 1) -> None:
		'''
		Causes faults on an axis.

		Args:
			axis: The axis on which to cause faults.
			fault_mask: The mask of faults to cause on the axis.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(fault_mask)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_FaultThrow(self.__capi_controller, execution_task_index, axis, fault_mask))

	def taskclearerror(self, task_index: int, execution_task_index: int = 1) -> None:
		'''
		Clears the task error that is set on the given task.

		Args:
			task_index: The task index on which to clear the task error.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TaskClearError(self.__capi_controller, execution_task_index, task_index))

	def taskclearwarning(self, task_index: int, execution_task_index: int = 1) -> None:
		'''
		Clears the task warning that is set on the given task.

		Args:
			task_index: The task index on which to clear the task warning.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TaskClearWarning(self.__capi_controller, execution_task_index, task_index))

	def taskseterror(self, task_index: int, error: int, execution_task_index: int = 1) -> None:
		'''
		Causes a specified task error on a task.

		Args:
			task_index: The task on which to cause a task error.
			error: The task error to cause. Specify 0 to clear the current task error.
			execution_task_index: The index of the task to execute the AeroScript command on.
		
		This command is deprecated and will be removed in the next major version of Automation1 software. This function overload has been obsoleted by the TaskSetError($taskIndex as integer, $errorMessage as string) overload. Use that overload instead to set a task error with your own specified message. Use the TaskClearError($taskIndex as integer) function to clear a task error.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(task_index)
		argument_checking.validate_int_64(error)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TaskSetError(self.__capi_controller, execution_task_index, task_index, error))

	def taskseterrorwithmessage(self, task_index: int, error_message: str, execution_task_index: int = 1) -> None:
		'''
		Causes a task error with the specified message on a task.

		Args:
			task_index: The task on which to cause a task error.
			error_message: The error message to display.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TaskSetErrorWithMessage(self.__capi_controller, execution_task_index, task_index, ctypes.create_string_buffer(bytes(error_message, 'utf-8'))))

	def tasksetwarning(self, task_index: int, warning: int, execution_task_index: int = 1) -> None:
		'''
		Causes a specified task warning on a task.

		Args:
			task_index: The task on which to cause a task warning.
			warning: The task warning to cause. Specify 0 to clear the current task warning.
			execution_task_index: The index of the task to execute the AeroScript command on.
		
		This command is deprecated and will be removed in the next major version of Automation1 software. This function overload has been obsoleted by the TaskSetWarning($taskIndex as integer, $warningMessage as string) overload. Use that overload instead to set a task warning with your own specified message. Use the TaskClearWarning($taskIndex as integer) function to clear a task warning.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(task_index)
		argument_checking.validate_int_64(warning)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TaskSetWarning(self.__capi_controller, execution_task_index, task_index, warning))

	def tasksetwarningwithmessage(self, task_index: int, warning_message: str, execution_task_index: int = 1) -> None:
		'''
		Causes a task warning with the specified message on a task.

		Args:
			task_index: The task on which to cause a task warning.
			warning_message: The warning message to display.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_TaskSetWarningWithMessage(self.__capi_controller, execution_task_index, task_index, ctypes.create_string_buffer(bytes(warning_message, 'utf-8'))))

	#endregion Methods

class MotionSetupCommands():
	'''
	A class to execute MotionSetup AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def setupaxisramptype(self, axis: Union[int, str], ramp_type_accel: RampType, ramp_type_arg_accel: float, ramp_type_decel: RampType, ramp_type_arg_decel: float, execution_task_index: int = 1) -> None:
		'''
		Sets a ramp type along with a ramp type value for accelerations and decelerations separately for an axis.

		Args:
			axis: The axis on which to set the ramp type.
			ramp_type_accel: The ramping type to set during accelerations.
			ramp_type_arg_accel: The ramping type additional argument for accelerations. This is only used when $rampTypeAccel is RampType.SCurve and represents the s-curve percentage.
			ramp_type_decel: The ramping type to set during decelerations.
			ramp_type_arg_decel: The ramping type additional argument for decelerations. This is only used when $rampTypeDecel is RampType.SCurve and represents the s-curve percentage.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(ramp_type_accel)
		argument_checking.validate_int_32(ramp_type_decel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupAxisRampType(self.__capi_controller, execution_task_index, axis, ramp_type_accel, ramp_type_arg_accel, ramp_type_decel, ramp_type_arg_decel))

	def setupaxisrampvalue(self, axis: Union[int, str], ramp_mode_accel: RampMode, ramp_value_accel: float, ramp_mode_decel: RampMode, ramp_value_decel: float, execution_task_index: int = 1) -> None:
		'''
		Sets a ramp value for accelerations and decelerations separately for an axis.

		Args:
			axis: The axis on which to set the ramp value.
			ramp_mode_accel: The ramping mode to set during accelerations.
			ramp_value_accel: The ramp value to set during accelerations.
			ramp_mode_decel: The ramping mode to set during decelerations.
			ramp_value_decel: The ramp value to set during decelerations.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(ramp_mode_accel)
		argument_checking.validate_int_32(ramp_mode_decel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupAxisRampValue(self.__capi_controller, execution_task_index, axis, ramp_mode_accel, ramp_value_accel, ramp_mode_decel, ramp_value_decel))

	def setupaxisspeed(self, axis: Union[int, str], speed: float, execution_task_index: int = 1) -> None:
		'''
		Sets the speed of an axis for MoveRapid() motion.

		Args:
			axis: The axis on which to set the speed.
			speed: The speed to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupAxisSpeed(self.__capi_controller, execution_task_index, axis, speed))

	def setupcoordinatedaccellimit(self, accel_limit_non_tangent: float, accel_limit_circular: float, execution_task_index: int = 1) -> None:
		'''
		Sets the maximum acceleration of coordinated motion on dominant axes on the current task.

		Args:
			accel_limit_non_tangent: The maximum acceleration of axes at non-tangent portions of a motion path.
			accel_limit_circular: The maximum acceleration of axes at curved parts of a motion path.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupCoordinatedAccelLimit(self.__capi_controller, execution_task_index, accel_limit_non_tangent, accel_limit_circular))

	def setupcoordinatedramptype(self, ramp_type_accel: RampType, ramp_type_arg_accel: float, ramp_type_decel: RampType, ramp_type_arg_decel: float, execution_task_index: int = 1) -> None:
		'''
		Sets a coordinated ramp type along with a ramp type value for accelerations and decelerations separately for dominant axes on the current task.

		Args:
			ramp_type_accel: The ramping type to set during accelerations.
			ramp_type_arg_accel: The ramping type additional argument for accelerations. This is only used when $rampTypeAccel is RampType.SCurve and represents the s-curve percentage.
			ramp_type_decel: The ramping type to set during decelerations.
			ramp_type_arg_decel: The ramping type additional argument for decelerations. This is only used when $rampTypeDecel is RampType.SCurve and represents the s-curve percentage.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(ramp_type_accel)
		argument_checking.validate_int_32(ramp_type_decel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupCoordinatedRampType(self.__capi_controller, execution_task_index, ramp_type_accel, ramp_type_arg_accel, ramp_type_decel, ramp_type_arg_decel))

	def setupcoordinatedrampvalue(self, ramp_mode_accel: RampMode, ramp_value_accel: float, ramp_mode_decel: RampMode, ramp_value_decel: float, execution_task_index: int = 1) -> None:
		'''
		Sets a coordinated ramp value for accelerations and decelerations separately for dominant axes on the current task.

		Args:
			ramp_mode_accel: The ramping mode to set during accelerations.
			ramp_value_accel: The ramp value to set during accelerations.
			ramp_mode_decel: The ramping mode to set during decelerations.
			ramp_value_decel: The ramp value to set during decelerations.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(ramp_mode_accel)
		argument_checking.validate_int_32(ramp_mode_decel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupCoordinatedRampValue(self.__capi_controller, execution_task_index, ramp_mode_accel, ramp_value_accel, ramp_mode_decel, ramp_value_decel))

	def setupcoordinatedspeed(self, speed: float, execution_task_index: int = 1) -> None:
		'''
		Sets the coordinated speed for dominant axes on the current task.

		Args:
			speed: The speed to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupCoordinatedSpeed(self.__capi_controller, execution_task_index, speed))

	def setupdependentcoordinatedaccellimit(self, accel_limit_dependent: float, execution_task_index: int = 1) -> None:
		'''
		Sets the maximum acceleration of coordinated motion on dependent axes on the current task.

		Args:
			accel_limit_dependent: The maximum acceleration of axes at all portions of a motion path.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupDependentCoordinatedAccelLimit(self.__capi_controller, execution_task_index, accel_limit_dependent))

	def setupdependentcoordinatedramprate(self, ramp_value_accel: float, ramp_value_decel: float, execution_task_index: int = 1) -> None:
		'''
		Sets a coordinated ramp rate for accelerations and decelerations separately for dependent axes on the current task.

		Args:
			ramp_value_accel: The ramp rate value to set during accelerations.
			ramp_value_decel: The ramp rate value to set during decelerations.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupDependentCoordinatedRampRate(self.__capi_controller, execution_task_index, ramp_value_accel, ramp_value_decel))

	def setupdependentcoordinatedspeed(self, speed: float, execution_task_index: int = 1) -> None:
		'''
		Sets the coordinated speed for dependent axes on the current task.

		Args:
			speed: The speed to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupDependentCoordinatedSpeed(self.__capi_controller, execution_task_index, speed))

	def setuptaskdistanceunits(self, distance_units: DistanceUnits, execution_task_index: int = 1) -> None:
		'''
		Sets the distance units of the current task.

		Args:
			distance_units: The distance units to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(distance_units)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupTaskDistanceUnits(self.__capi_controller, execution_task_index, distance_units))

	def setuptasktargetmode(self, target_mode: TargetMode, execution_task_index: int = 1) -> None:
		'''
		Sets the target mode of the current task.

		Args:
			target_mode: The target mode to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(target_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupTaskTargetMode(self.__capi_controller, execution_task_index, target_mode))

	def setuptasktimeunits(self, time_units: TimeUnits, execution_task_index: int = 1) -> None:
		'''
		Sets the time units of the current task.

		Args:
			time_units: The time units to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(time_units)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupTaskTimeUnits(self.__capi_controller, execution_task_index, time_units))

	def setuptaskwaitmode(self, wait_mode: WaitMode, execution_task_index: int = 1) -> None:
		'''
		Sets the wait mode of the current task.

		Args:
			wait_mode: The wait mode to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(wait_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SetupTaskWaitMode(self.__capi_controller, execution_task_index, wait_mode))

	#endregion Methods

class SafeZoneCommands():
	'''
	A class to execute SafeZone AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def safezoneboundaryadd(self, zone: int, axis: Union[int, str], lower_bound: float, upper_bound: float, execution_task_index: int = 1) -> None:
		'''
		Adds a boundary to the specified safe zone.

		Args:
			zone: The index of the safe zone on which to add a boundary.
			axis: The axis that represents the boundary to add.
			lower_bound: The safe zone lower boundary, specified in user units.
			upper_bound: The safe zone upper boundary, specified in user units.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(zone)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SafeZoneBoundaryAdd(self.__capi_controller, execution_task_index, zone, axis, lower_bound, upper_bound))

	def safezoneboundaryremove(self, zone: int, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Removes the specified boundary from the specified safe zone.

		Args:
			zone: The index of the safe zone on which to remove a boundary.
			axis: The axis that represents the boundary to remove.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(zone)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SafeZoneBoundaryRemove(self.__capi_controller, execution_task_index, zone, axis))

	def safezoneboundaryremoveall(self, zone: int, execution_task_index: int = 1) -> None:
		'''
		Removes all boundaries from the specified safe zone.

		Args:
			zone: The index of the safe zone on which to remove all boundaries.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(zone)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SafeZoneBoundaryRemoveAll(self.__capi_controller, execution_task_index, zone))

	def safezoneoff(self, zone: int, execution_task_index: int = 1) -> None:
		'''
		Disables the specified safe zone.

		Args:
			zone: The safe zone to disable.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(zone)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SafeZoneOff(self.__capi_controller, execution_task_index, zone))

	def safezoneon(self, zone: int, execution_task_index: int = 1) -> None:
		'''
		Enables the specified safe zone.

		Args:
			zone: The safe zone to enable.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(zone)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SafeZoneOn(self.__capi_controller, execution_task_index, zone))

	def safezonesettype(self, zone: int, zone_type: SafeZoneType, execution_task_index: int = 1) -> None:
		'''
		Sets the safe zone type for the specified safe zone.

		Args:
			zone: The safe zone on which to set the safe zone type.
			zone_type: The safe zone type to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(zone)
		argument_checking.validate_int_32(zone_type)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_SafeZoneSetType(self.__capi_controller, execution_task_index, zone, zone_type))

	#endregion Methods

class TransformationCommands():
	'''
	A class to execute Transformation AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def ctransformationdisable(self, transformation_name: str, execution_task_index: int = 1) -> None:
		'''
		Disable a C transformation. This will stop running inverse and forward computations for this transformation.

		Args:
			transformation_name: The name specified in the C Transformation configuration.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CTransformationDisable(self.__capi_controller, execution_task_index, ctypes.create_string_buffer(bytes(transformation_name, 'utf-8'))))

	def ctransformationenable(self, transformation_name: str, execution_task_index: int = 1) -> None:
		'''
		Enable a C transformation. This will begin running inverse and forward computations for the specified transformation. All axes part of the transformation must be enabled at any time the transformation is enabled. If the transformation is enabled while there is synchronous motion on the same task, then the motion program will wait for motion to complete before enabling the transformation.

		Args:
			transformation_name: The name specified in the C Transformation configuration.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CTransformationEnable(self.__capi_controller, execution_task_index, ctypes.create_string_buffer(bytes(transformation_name, 'utf-8'))))

	def ctransformationgetproperty(self, transformation_name: str, property_: str, execution_task_index: int = 1) -> float:
		'''
		Call the OnGetProperty() C function defined in a C transformation.

		Args:
			transformation_name: The name specified in the C Transformation configuration.
			property_: The property argument provided to the OnGetProperty() C function.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value argument set by the OnGetProperty() C function.
		'''
		argument_checking.validate_int_32(execution_task_index)
		returnOut = ctypes.pointer(ctypes.c_double())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CTransformationGetProperty(self.__capi_controller, execution_task_index, ctypes.create_string_buffer(bytes(transformation_name, 'utf-8')), ctypes.create_string_buffer(bytes(property_, 'utf-8')), returnOut))
		return returnOut.contents.value

	def ctransformationsetinputaxes(self, transformation_name: str, input_axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Set the input axes of a C transformation.

		Args:
			transformation_name: The name specified in the C Transformation configuration.
			input_axes: The input axes of the transformation. Motion from these axes are input to the transformation.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		input_axes = AxisInputCollection(input_axes).to_axis_indices(self.__capi_controller)
		input_axes_c_array = c_helpers.create_c_array(ctypes.c_int32, input_axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(input_axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CTransformationSetInputAxes(self.__capi_controller, execution_task_index, ctypes.create_string_buffer(bytes(transformation_name, 'utf-8')), input_axes_c_array, len(input_axes)))

	def ctransformationsetoutputaxes(self, transformation_name: str, output_axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Set the output axes of a C transformation.

		Args:
			transformation_name: The name specified in the C Transformation configuration.
			output_axes: The output axes of the transformation. The transformation outputs motion to these axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		output_axes = AxisInputCollection(output_axes).to_axis_indices(self.__capi_controller)
		output_axes_c_array = c_helpers.create_c_array(ctypes.c_int32, output_axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(output_axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CTransformationSetOutputAxes(self.__capi_controller, execution_task_index, ctypes.create_string_buffer(bytes(transformation_name, 'utf-8')), output_axes_c_array, len(output_axes)))

	def ctransformationsetproperty(self, transformation_name: str, property_: str, value: float, execution_task_index: int = 1) -> None:
		'''
		Call the OnSetProperty() C function defined in a C transformation.

		Args:
			transformation_name: The name specified in the C Transformation configuration.
			property_: The property argument provided to the OnSetProperty() C function.
			value: The value argument provided to the OnSetProperty() C function.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CTransformationSetProperty(self.__capi_controller, execution_task_index, ctypes.create_string_buffer(bytes(transformation_name, 'utf-8')), ctypes.create_string_buffer(bytes(property_, 'utf-8')), value))

	#endregion Methods

class CalibrationCommands():
	'''
	A class to execute Calibration AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def calibrationload(self, calibration_type: CalibrationType, controller_file_name: str, execution_task_index: int = 1) -> None:
		'''
		Loads and activates the specified axis calibration file or galvo power correction file.

		Args:
			calibration_type: The type of calibration that the specified file represents.
			controller_file_name: The path to the file to be loaded as a calibration file.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(calibration_type)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CalibrationLoad(self.__capi_controller, execution_task_index, calibration_type, ctypes.create_string_buffer(bytes(controller_file_name, 'utf-8'))))

	def calibrationunload(self, calibration_type: CalibrationType, execution_task_index: int = 1) -> None:
		'''
		Deactivates and unloads the calibration for the specified calibration type.

		Args:
			calibration_type: The type of calibration to be unloaded.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(calibration_type)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_CalibrationUnload(self.__capi_controller, execution_task_index, calibration_type))

	#endregion Methods

class JoystickCommands():
	'''
	A class to execute Joystick AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def joystickaxisgroupadd(self, motion_axes: Union[int, str, Iterable[Union[int, str]]], joystick_inputs: List[JoystickInput], execution_task_index: int = 1) -> None:
		'''
		Adds an axis group configuration to the joystick configuration.

		Args:
			motion_axes: A list of one or more axes to control with the joystick.
			joystick_inputs: A list of one or more joystick inputs to use to control axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		motion_axes = AxisInputCollection(motion_axes).to_axis_indices(self.__capi_controller)
		motion_axes_c_array = c_helpers.create_c_array(ctypes.c_int32, motion_axes)
		joystick_inputs_c_array = c_helpers.create_c_array(ctypes.c_int32, joystick_inputs)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(motion_axes)
		argument_checking.validate_int_32(joystick_inputs)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_JoystickAxisGroupAdd(self.__capi_controller, execution_task_index, motion_axes_c_array, len(motion_axes), joystick_inputs_c_array, len(joystick_inputs)))

	def joystickaxisgroupremoveall(self, execution_task_index: int = 1) -> None:
		'''
		Removes all axis group configurations from the joystick configuration.

		Args:
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_JoystickAxisGroupRemoveAll(self.__capi_controller, execution_task_index))

	def joystickrun(self, execution_task_index: int = 1) -> None:
		'''
		Activates the joystick.

		Args:
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_JoystickRun(self.__capi_controller, execution_task_index))

	#endregion Methods

class DriveAnalogControlCommands():
	'''
	A class to execute DriveAnalogControl AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def driveanalogaccelerationfeedforwardconfigureinput(self, axis: Union[int, str], analog_input_num: int, input_scale: float, input_offset: float, execution_task_index: int = 1) -> None:
		'''
		Configures the relationship between the acceleration feedforward and analog input voltage, where Acceleration Feedforward = (Analog Input Voltage - ($inputOffset / 1000)) x $inputScale.

		Args:
			axis: The axis on which to apply the configuration for the Drive Analog Acceleration Feedforward feature.
			analog_input_num: The analog input signal used in the acceleration feedforward computation.
			input_scale: The scale value used in the acceleration feedforward computation to convert from volts to units/second^2.
			input_offset: The offset value in millivolts used in the acceleration feedforward computation. This argument has a minimum value of -1000 and a maximum value of 1000.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(analog_input_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogAccelerationFeedforwardConfigureInput(self.__capi_controller, execution_task_index, axis, analog_input_num, input_scale, input_offset))

	def driveanalogaccelerationfeedforwardoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the Drive Analog Acceleration Feedforward feature.

		Args:
			axis: The axis on which to disable the Drive Analog Acceleration Feedforward feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogAccelerationFeedforwardOff(self.__capi_controller, execution_task_index, axis))

	def driveanalogaccelerationfeedforwardon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the Drive Analog Acceleration Feedforward feature.

		Args:
			axis: The axis on which to enable the Drive Analog Acceleration Feedforward feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogAccelerationFeedforwardOn(self.__capi_controller, execution_task_index, axis))

	def driveanalogcurrentcontrolconfigureinput(self, axis: Union[int, str], analog_input_num: int, digital_input_num: int, input_scale: float, input_offset: float, execution_task_index: int = 1) -> None:
		'''
		Configures the relationship between the output current and analog input voltage, where Current = (Analog Input Voltage - ($inputOffset / 1000)) x $inputScale.

		Args:
			axis: The axis on which to apply the configuration for the Drive Analog Current Control feature.
			analog_input_num: The analog input signal used in the current computation.
			digital_input_num: The digital input signal used to enable and disable the axis.
			input_scale: The scale value used in the current computation to convert from volts to amps.
			input_offset: The offset value in millivolts used in the current computation. This argument has a minimum value of -1000 and a maximum value of 1000.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(analog_input_num)
		argument_checking.validate_int_64(digital_input_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogCurrentControlConfigureInput(self.__capi_controller, execution_task_index, axis, analog_input_num, digital_input_num, input_scale, input_offset))

	def driveanalogcurrentcontroloff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the Drive Analog Current Control feature.

		Args:
			axis: The axis on which to disable the Drive Analog Current Control feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogCurrentControlOff(self.__capi_controller, execution_task_index, axis))

	def driveanalogcurrentcontrolon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the Drive Analog Current Control feature.

		Args:
			axis: The axis on which to enable the Drive Analog Current Control feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogCurrentControlOn(self.__capi_controller, execution_task_index, axis))

	def driveanalogpositioncontrolconfigureinput(self, axis: Union[int, str], input_num: int, input_scale: float, input_offset: float, execution_task_index: int = 1) -> None:
		'''
		Configures the relationship between the output position and analog input voltage, where Position = (Analog Input Voltage - $inputOffset) x $inputScale + (Starting Position). Starting Position is the position of the axis at the time DriveAnalogPositionControlOn() is called.

		Args:
			axis: The axis on which to apply the configuration for the Drive Analog Position Control feature.
			input_num: The analog input signal used in the position computation.
			input_scale: The scale value used in the position computation.
			input_offset: The offset value used in the position computation.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(input_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogPositionControlConfigureInput(self.__capi_controller, execution_task_index, axis, input_num, input_scale, input_offset))

	def driveanalogpositioncontrolconfigurespeedclamp(self, axis: Union[int, str], max_speed: float, execution_task_index: int = 1) -> None:
		'''
		Configures the maximum speed at which the controller commands the axis to move using the Drive Analog Position Control feature. If you do not use this function, then the controller does not limit the maximum speed.

		Args:
			axis: The axis on which to apply the configuration for the Drive Analog Position Control feature.
			max_speed: The speed in user units per second. If you specify a value of 0 for this argument, then the controller does not limit the maximum speed.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogPositionControlConfigureSpeedClamp(self.__capi_controller, execution_task_index, axis, max_speed))

	def driveanalogpositioncontroloff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disable the Drive Analog Position Control feature.

		Args:
			axis: The axis on which to disable the Drive Analog Position Control feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogPositionControlOff(self.__capi_controller, execution_task_index, axis))

	def driveanalogpositioncontrolon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enable the Drive Analog Position Control feature.

		Args:
			axis: The axis on which to enable the Drive Analog Position Control feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogPositionControlOn(self.__capi_controller, execution_task_index, axis))

	def driveanalogvelocitycontrolconfigureinput(self, axis: Union[int, str], analog_input_num: int, digital_input_num: int, input_scale: float, input_offset: float, execution_task_index: int = 1) -> None:
		'''
		Configures the relationship between the output velocity and analog input voltage, where Velocity = (Analog Input Voltage - ($inputOffset / 1000)) x $inputScale.

		Args:
			axis: The axis on which to apply the configuration for the Drive Analog Velocity Control feature.
			analog_input_num: The analog input signal used in the velocity computation.
			digital_input_num: The digital input signal used to enable and disable the axis.
			input_scale: The scale value used in the velocity computation to convert from volts to units/second.
			input_offset: The offset value in millivolts used in the velocity computation. This argument has a minimum value of -1000 and a maximum value of 1000.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(analog_input_num)
		argument_checking.validate_int_64(digital_input_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogVelocityControlConfigureInput(self.__capi_controller, execution_task_index, axis, analog_input_num, digital_input_num, input_scale, input_offset))

	def driveanalogvelocitycontroloff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the Drive Analog Velocity Control feature.

		Args:
			axis: The axis on which to disable the Drive Analog Current Control feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogVelocityControlOff(self.__capi_controller, execution_task_index, axis))

	def driveanalogvelocitycontrolon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the Drive Analog Velocity Control feature.

		Args:
			axis: The axis on which to enable the Drive Analog Velocity Control feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogVelocityControlOn(self.__capi_controller, execution_task_index, axis))

	def driveanalogvelocityfeedforwardconfigureinput(self, axis: Union[int, str], analog_input_num: int, input_scale: float, input_offset: float, execution_task_index: int = 1) -> None:
		'''
		Configures the relationship between the velocity feedforward and analog input voltage, where Velocity Feedforward = (Analog Input Voltage - ($inputOffset / 1000)) x $inputScale.

		Args:
			axis: The axis on which to apply the configuration for the Drive Analog Velocity Feedforward feature.
			analog_input_num: The analog input signal used in the velocity feedforward computation.
			input_scale: The scale value used in the velocity feedforward computation to convert from volts to units/second.
			input_offset: The offset value in millivolts used in the velocity feedforward computation. This argument has a minimum value of -1000 and a maximum value of 1000.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(analog_input_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogVelocityFeedforwardConfigureInput(self.__capi_controller, execution_task_index, axis, analog_input_num, input_scale, input_offset))

	def driveanalogvelocityfeedforwardoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the Drive Analog Velocity Feedforward feature.

		Args:
			axis: The axis on which to disable the Drive Analog Velocity Feedforward feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogVelocityFeedforwardOff(self.__capi_controller, execution_task_index, axis))

	def driveanalogvelocityfeedforwardon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the Drive Analog Velocity Feedforward feature.

		Args:
			axis: The axis on which to enable the Drive Analog Velocity Feedforward feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DriveAnalogVelocityFeedforwardOn(self.__capi_controller, execution_task_index, axis))

	#endregion Methods

class AutofocusCommands():
	'''
	A class to execute Autofocus AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def autofocusoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables autofocus on an axis.

		Args:
			axis: The axis on which to disable autofocus.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AutofocusOff(self.__capi_controller, execution_task_index, axis))

	def autofocuson(self, axis: Union[int, str], focus_mode: AutofocusFocusMode, execution_task_index: int = 1) -> None:
		'''
		Enables autofocus on an axis.

		Args:
			axis: The axis on which to enable autofocus.
			focus_mode: Selects if autofocus will run in continuous focus or single focus mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(focus_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AutofocusOn(self.__capi_controller, execution_task_index, axis, focus_mode))

	#endregion Methods

class PsoCommands():
	'''
	A class to execute Pso AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def psobitmapconfigurearray(self, axis: Union[int, str], drive_array_start_address: int, number_of_points: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures an array of PSO bit data words, where each word is a 32-bit integer.

		Args:
			axis: The axis on which to configure the bit data.
			drive_array_start_address: The byte-addressable index of the drive array where the first word of bit data is stored.
			number_of_points: The number of bit data words to be read from the drive array.
			enable_repeat: Configures PSO to continue to use bit data words after the last word in the array is used, starting over at the first word.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_points)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoBitmapConfigureArray(self.__capi_controller, execution_task_index, axis, drive_array_start_address, number_of_points, enable_repeat))

	def psodistanceconfigureallowedeventdirection(self, axis: Union[int, str], event_direction: PsoDistanceAllowedEventDirection, execution_task_index: int = 1) -> None:
		'''
		Configures the distance counter tracking directions that will cause PSO distance events.

		Args:
			axis: The axis on which to configure the distance event directions.
			event_direction: The distance event directions to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(event_direction)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceConfigureAllowedEventDirection(self.__capi_controller, execution_task_index, axis, event_direction))

	def psodistanceconfigurearraydistances(self, axis: Union[int, str], drive_array_start_address: int, number_of_distances: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures an array of distances in counts that the PSO counter or counters must travel for an event to occur.

		Args:
			axis: The axis on which to configure the distances.
			drive_array_start_address: The byte-addressable index of the drive array where the first distance is stored.
			number_of_distances: The number of distances to be read from the drive array.
			enable_repeat: Configures PSO to continue to use distances after the last distance in the array is used, starting over at the first distance.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_distances)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceConfigureArrayDistances(self.__capi_controller, execution_task_index, axis, drive_array_start_address, number_of_distances, enable_repeat))

	def psodistanceconfigurecounterreset(self, axis: Union[int, str], options_mask: int, execution_task_index: int = 1) -> None:
		'''
		Configures the conditions which will reset the PSO distance counters.

		Args:
			axis: The axis on which to configure the distance counter reset conditions.
			options_mask: A bitmask of PSO distance counter reset options. Use the values from the PsoDistanceCounterResetMask enum.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(options_mask)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceConfigureCounterReset(self.__capi_controller, execution_task_index, axis, options_mask))

	def psodistanceconfigurefixeddistance(self, axis: Union[int, str], distance: int, execution_task_index: int = 1) -> None:
		'''
		Configures the distance in counts that the PSO counter or counters must travel for an event to occur.

		Args:
			axis: The axis on which to configure the distance.
			distance: The distance in counts.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(distance)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceConfigureFixedDistance(self.__capi_controller, execution_task_index, axis, distance))

	def psodistanceconfigureinputs(self, axis: Union[int, str], inputs: List[PsoDistanceInput], execution_task_index: int = 1) -> None:
		'''
		Selects the source of each PSO distance counter.

		Args:
			axis: The axis on which to configure the distance counter sources.
			inputs: A list of one to three input sources, one for each distance counter.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		inputs_c_array = c_helpers.create_c_array(ctypes.c_int32, inputs)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(inputs)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceConfigureInputs(self.__capi_controller, execution_task_index, axis, inputs_c_array, len(inputs)))

	def psodistanceconfigurescaling(self, axis: Union[int, str], scale_factors: List[int], execution_task_index: int = 1) -> None:
		'''
		Configures the PSO distance counters to apply an integer scale factor for each tracking input.

		Args:
			axis: The axis on which to configure the scale factors.
			scale_factors: A list of one to three integer scale factors, one per tracking input.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		scale_factors_c_array = c_helpers.create_c_array(ctypes.c_int64, scale_factors)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(scale_factors)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceConfigureScaling(self.__capi_controller, execution_task_index, axis, scale_factors_c_array, len(scale_factors)))

	def psodistancecounteroff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the PSO distance counters, causing them to retain their values and ignore their configured inputs.

		Args:
			axis: The axis on which to disable the PSO distance counters.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceCounterOff(self.__capi_controller, execution_task_index, axis))

	def psodistancecounteron(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the PSO distance counters, allowing them to track their configured inputs.

		Args:
			axis: The axis on which to enable the PSO distance counters.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceCounterOn(self.__capi_controller, execution_task_index, axis))

	def psodistanceeventsoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables PSO distance events.

		Args:
			axis: The axis on which to disable distance events.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceEventsOff(self.__capi_controller, execution_task_index, axis))

	def psodistanceeventson(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables PSO distance events.

		Args:
			axis: The axis on which to enable distance events.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoDistanceEventsOn(self.__capi_controller, execution_task_index, axis))

	def psoeventconfiguremask(self, axis: Union[int, str], event_mask: int, execution_task_index: int = 1) -> None:
		'''
		Configures additional conditions to prevent PSO events from occurring.

		Args:
			axis: The axis on which to configure the event mask conditions.
			event_mask: A bitmask of event mask conditions. Use the values from the PsoEventMask enum.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(event_mask)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoEventConfigureMask(self.__capi_controller, execution_task_index, axis, event_mask))

	def psoeventcontinuousoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Immediately halts active continuous PSO events.

		Args:
			axis: The axis on which to halt the events.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoEventContinuousOff(self.__capi_controller, execution_task_index, axis))

	def psoeventcontinuouson(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Immediately causes continuous PSO events to occur.

		Args:
			axis: The axis on which to cause the events.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoEventContinuousOn(self.__capi_controller, execution_task_index, axis))

	def psoeventgeneratesingle(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Immediately causes a single PSO event to occur.

		Args:
			axis: The axis on which to cause the event.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoEventGenerateSingle(self.__capi_controller, execution_task_index, axis))

	def psolasereventsoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables PSO laser events.

		Args:
			axis: The axis on which to disable PSO laser events.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoLaserEventsOff(self.__capi_controller, execution_task_index, axis))

	def psolasereventson(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Configures the PSO to generate an event when the laser command bit turns on.

		Args:
			axis: The axis on which to generate laser PSO events.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoLaserEventsOn(self.__capi_controller, execution_task_index, axis))

	def psooutputconfigureoutput(self, axis: Union[int, str], output: PsoOutputPin, execution_task_index: int = 1) -> None:
		'''
		Selects the output pin on which to drive the PSO output.

		Args:
			axis: The axis on which to select the PSO output pin.
			output: The selected output pin.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(output)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoOutputConfigureOutput(self.__capi_controller, execution_task_index, axis, output))

	def psooutputconfiguresource(self, axis: Union[int, str], output_source: PsoOutputSource, execution_task_index: int = 1) -> None:
		'''
		Selects which internal PSO signal to drive onto the output pin.

		Args:
			axis: The axis on which to select the PSO output source.
			output_source: The selected output source.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(output_source)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoOutputConfigureSource(self.__capi_controller, execution_task_index, axis, output_source))

	def psooutputoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Immediately deactivates the PSO output.

		Args:
			axis: The axis on which to deactivate the PSO output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoOutputOff(self.__capi_controller, execution_task_index, axis))

	def psooutputon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Immediately activates the PSO output.

		Args:
			axis: The axis on which to activate the PSO output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoOutputOn(self.__capi_controller, execution_task_index, axis))

	def psoreset(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Resets all PSO configuration, which restores all PSO settings to their default values.

		Args:
			axis: The axis on which to reset the PSO configuration.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoReset(self.__capi_controller, execution_task_index, axis))

	def psotransformationconfigure(self, axis: Union[int, str], transformation_channel: int, input_a: PsoTransformationInput, input_b: PsoTransformationInput, transformation_function: PsoTransformationFunction, execution_task_index: int = 1) -> None:
		'''
		Configures a PSO input transformation channel.

		Args:
			axis: The axis on which to configure the transformation channel.
			transformation_channel: The transformation channel to configure.
			input_a: The first input to the transformation.
			input_b: The second input to the transformation.
			transformation_function: The function of the transformation.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(transformation_channel)
		argument_checking.validate_int_32(input_a)
		argument_checking.validate_int_32(input_b)
		argument_checking.validate_int_32(transformation_function)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoTransformationConfigure(self.__capi_controller, execution_task_index, axis, transformation_channel, input_a, input_b, transformation_function))

	def psotransformationoff(self, axis: Union[int, str], transformation_channel: int, execution_task_index: int = 1) -> None:
		'''
		Disables a PSO input transformation channel.

		Args:
			axis: The axis on which to disable the transformation channel.
			transformation_channel: The transformation channel to disable.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(transformation_channel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoTransformationOff(self.__capi_controller, execution_task_index, axis, transformation_channel))

	def psotransformationon(self, axis: Union[int, str], transformation_channel: int, execution_task_index: int = 1) -> None:
		'''
		Enables a PSO input transformation channel.

		Args:
			axis: The axis on which to enable the transformation channel.
			transformation_channel: The transformation channel to enable.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(transformation_channel)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoTransformationOn(self.__capi_controller, execution_task_index, axis, transformation_channel))

	def psowaveformapplypulseconfiguration(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Checks for a valid configuration of pulse mode parameters and applies the configuration to the waveform module.

		Args:
			axis: The axis on which to apply the pulse configuration.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformApplyPulseConfiguration(self.__capi_controller, execution_task_index, axis))

	def psowaveformapplypwmconfiguration(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Checks for a valid configuration of PWM mode parameters and applies the configuration to the waveform module.

		Args:
			axis: The axis on which to apply the PWM configuration.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformApplyPwmConfiguration(self.__capi_controller, execution_task_index, axis))

	def psowaveformconfiguredelay(self, axis: Union[int, str], delay_time: float, execution_task_index: int = 1) -> None:
		'''
		Configures the waveform module to wait for the specified time after a PSO event before beginning to output a waveform.

		Args:
			axis: The axis on which to configure the waveform output delay.
			delay_time: The delay time in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigureDelay(self.__capi_controller, execution_task_index, axis, delay_time))

	def psowaveformconfiguremode(self, axis: Union[int, str], waveform_mode: PsoWaveformMode, execution_task_index: int = 1) -> None:
		'''
		Selects the output mode of the waveform module.

		Args:
			axis: The axis on which to select the output mode of the waveform module.
			waveform_mode: Mode selection for the waveform module output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(waveform_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigureMode(self.__capi_controller, execution_task_index, axis, waveform_mode))

	def psowaveformconfigurepulsearraycounts(self, axis: Union[int, str], drive_array_start_address: int, number_of_points: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures an array of pulse counts for a sequence of waveform module outputs in pulse mode. The pulse count specifies the number of periods that will be generated from a single PSO event.

		Args:
			axis: The axis on which to configure the pulse counts.
			drive_array_start_address: The byte-addressable index of the drive array where the first pulse count is stored.
			number_of_points: The number of pulse counts to be read from the drive array.
			enable_repeat: Configures PSO to continue to use pulse counts after the last pulse count in the array is used, starting over at the first pulse count.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_points)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseArrayCounts(self.__capi_controller, execution_task_index, axis, drive_array_start_address, number_of_points, enable_repeat))

	def psowaveformconfigurepulsearrayontimes(self, axis: Union[int, str], drive_array_start_address: int, number_of_points: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures an array of on times for a sequence of waveform module outputs in pulse mode. The on time specifies the active portion of the pulse period.

		Args:
			axis: The axis on which to configure the on times.
			drive_array_start_address: The byte-addressable index of the drive array where the first on time is stored.
			number_of_points: The number of on times to be read from the drive array.
			enable_repeat: Configures PSO to continue to use on times after the last on time in the array is used, starting over at the first on time.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_points)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseArrayOnTimes(self.__capi_controller, execution_task_index, axis, drive_array_start_address, number_of_points, enable_repeat))

	def psowaveformconfigurepulsearraytotaltimes(self, axis: Union[int, str], drive_array_start_address: int, number_of_points: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures an array of total times for a sequence of waveform module outputs in pulse mode. The total time specifies the full period of the pulse.

		Args:
			axis: The axis on which to configure the total times.
			drive_array_start_address: The byte-addressable index of the drive array where the first total time is stored.
			number_of_points: The number of total times to be read from the drive array.
			enable_repeat: Configures PSO to continue to use total times after the last total time in the array is used, starting over at the first total time.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_points)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseArrayTotalTimes(self.__capi_controller, execution_task_index, axis, drive_array_start_address, number_of_points, enable_repeat))

	def psowaveformconfigurepulseeventqueue(self, axis: Union[int, str], max_queued_events: int, execution_task_index: int = 1) -> None:
		'''
		Configures the maximum number of events in the queue. Each event in the queue will cause a PSO waveform pulse generation to occur after the active waveform period completes.

		Args:
			axis: The axis on which to configure the queue for the PSO waveform pulse event.
			max_queued_events: The maximum number of events to put in the queue.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(max_queued_events)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseEventQueue(self.__capi_controller, execution_task_index, axis, max_queued_events))

	def psowaveformconfigurepulsefixedcount(self, axis: Union[int, str], pulse_count: int, execution_task_index: int = 1) -> None:
		'''
		Configures the fixed pulse count of the waveform module output in pulse mode, which will be applied to all pulses. The pulse count specifies the number of periods that will be generated from a single PSO event.

		Args:
			axis: The axis on which to configure the number of pulses.
			pulse_count: The integer number of pulses.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(pulse_count)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseFixedCount(self.__capi_controller, execution_task_index, axis, pulse_count))

	def psowaveformconfigurepulsefixedontime(self, axis: Union[int, str], on_time: float, execution_task_index: int = 1) -> None:
		'''
		Configures the fixed on time of the waveform module output in pulse mode, which will be applied to all pulses. The on time specifies the active portion of the pulse period.

		Args:
			axis: The axis on which to configure the on time.
			on_time: The on time in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseFixedOnTime(self.__capi_controller, execution_task_index, axis, on_time))

	def psowaveformconfigurepulsefixedtotaltime(self, axis: Union[int, str], total_time: float, execution_task_index: int = 1) -> None:
		'''
		Configures the fixed total time of the waveform module output in pulse mode, which will be applied to all pulses. The total time specifies the full period of the pulse.

		Args:
			axis: The axis on which to configure the total time.
			total_time: The total time in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseFixedTotalTime(self.__capi_controller, execution_task_index, axis, total_time))

	def psowaveformconfigurepulsemask(self, axis: Union[int, str], pulse_mask: int, execution_task_index: int = 1) -> None:
		'''
		Configures additional conditions to disable the PSO waveform output in pulse mode.

		Args:
			axis: The axis on which to configure PSO waveform pulse mode masking options.
			pulse_mask: A bitmask of PSO waveform pulse mode masking options. Use the values from the PsoWaveformPulseMask enum.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(pulse_mask)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseMask(self.__capi_controller, execution_task_index, axis, pulse_mask))

	def psowaveformconfigurepulsetruncation(self, axis: Union[int, str], prevent_truncation: int, execution_task_index: int = 1) -> None:
		'''
		Allows or prevents the waveform module from outputting truncated waveform outputs in pulse mode.

		Args:
			axis: The axis on which to configure the pulse truncation prevention feature.
			prevent_truncation: Configures the waveform module to not allow the generation of truncated waveform outputs in pulse mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(prevent_truncation)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePulseTruncation(self.__capi_controller, execution_task_index, axis, prevent_truncation))

	def psowaveformconfigurepwmontimes(self, axis: Union[int, str], drive_array_start_address: int, number_of_points: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures an array of on times for a sequence of waveform module outputs in PWM mode. The on time specifies the variable active portion of the PWM signal.

		Args:
			axis: The axis on which to configure the on times.
			drive_array_start_address: The byte-addressable index of the drive array where the first on time is stored.
			number_of_points: The number of on times to be read from the drive array.
			enable_repeat: Configures PSO to continue to use on times after the last on time in the array is used, starting over at the first on time.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_points)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePwmOnTimes(self.__capi_controller, execution_task_index, axis, drive_array_start_address, number_of_points, enable_repeat))

	def psowaveformconfigurepwmtotaltime(self, axis: Union[int, str], total_time: float, execution_task_index: int = 1) -> None:
		'''
		Configures the fixed total time of the waveform module output in PWM mode. The total time specifies the full period of the PWM signal.

		Args:
			axis: The axis on which to configure the total time.
			total_time: The total time in microseconds.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformConfigurePwmTotalTime(self.__capi_controller, execution_task_index, axis, total_time))

	def psowaveformexternalsyncconfiguredelaymode(self, axis: Union[int, str], delay_mode: PsoWaveformExternalSyncDelayMode, execution_task_index: int = 1) -> None:
		'''
		Configures the delay mode of the waveform module when you use the external synchronization signal.

		Args:
			axis: The axis on which to configure the external sync delay mode.
			delay_mode: The external sync delay mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(delay_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformExternalSyncConfigureDelayMode(self.__capi_controller, execution_task_index, axis, delay_mode))

	def psowaveformexternalsyncoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the external sync option for the waveform module.

		Args:
			axis: The axis on which to disable external sync option.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformExternalSyncOff(self.__capi_controller, execution_task_index, axis))

	def psowaveformexternalsyncon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Configures the waveform module to wait for the rising edge of the external sync signal before beginning to output a waveform.

		Args:
			axis: The axis on which to enable external sync option.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformExternalSyncOn(self.__capi_controller, execution_task_index, axis))

	def psowaveformoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Disables the waveform module, preventing PSO events from triggering it.

		Args:
			axis: The axis on which to disable the waveform module.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformOff(self.__capi_controller, execution_task_index, axis))

	def psowaveformon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Enables the waveform module, allowing PSO events to trigger it.

		Args:
			axis: The axis on which to enable the waveform module.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformOn(self.__capi_controller, execution_task_index, axis))

	def psowaveformscalingconfigure(self, axis: Union[int, str], scaling_mode: PsoWaveformScalingMode, scaling_input: PsoWaveformScalingInput, input_range: List[float], scale_factor_range: List[float], execution_task_index: int = 1) -> None:
		'''
		Specifies the configuration of the optional PSO waveform scaling feature.

		Args:
			axis: The axis on which to configure PSO waveform scaling.
			scaling_mode: Specifies the waveform parameters to which to apply the PSO waveform scaling.
			scaling_input: Specifies the input to the PSO waveform scaling.
			input_range: Specifies the range of values in which the configured input will be used to calculate the scale factor to apply to the waveform parameters.
			scale_factor_range: Specifies the valid range of scale factor outputs from the PSO waveform scaling feature.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		input_range_c_array = c_helpers.create_c_array(ctypes.c_double, input_range)
		scale_factor_range_c_array = c_helpers.create_c_array(ctypes.c_double, scale_factor_range)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(scaling_mode)
		argument_checking.validate_int_32(scaling_input)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformScalingConfigure(self.__capi_controller, execution_task_index, axis, scaling_mode, scaling_input, input_range_c_array, len(input_range), scale_factor_range_c_array, len(scale_factor_range)))

	def psowaveformscalingoff(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Deactivates PSO waveform scaling.

		Args:
			axis: The axis on which to deactivate PSO waveform scaling.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformScalingOff(self.__capi_controller, execution_task_index, axis))

	def psowaveformscalingon(self, axis: Union[int, str], execution_task_index: int = 1) -> None:
		'''
		Activates PSO waveform scaling.

		Args:
			axis: The axis on which to activate PSO waveform scaling.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWaveformScalingOn(self.__capi_controller, execution_task_index, axis))

	def psowindowconfigurearrayranges(self, axis: Union[int, str], window_number: int, drive_array_start_address: int, number_of_ranges: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures an array of window range pairs each consisting of a lower bound followed by an upper bound.

		Args:
			axis: The axis on which to configure the window ranges.
			window_number: The number of the window on which to configure the ranges.
			drive_array_start_address: The byte-addressable index of the drive array where the lower bound of the first range pair is stored.
			number_of_ranges: The number of range value pairs to be read from the drive array.
			enable_repeat: Configures PSO to continue to use range pairs after the last range pair in the array is used, starting over at the first range pair.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(window_number)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_ranges)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowConfigureArrayRanges(self.__capi_controller, execution_task_index, axis, window_number, drive_array_start_address, number_of_ranges, enable_repeat))

	def psowindowconfigurearrayupdatedirection(self, axis: Union[int, str], window_number: int, window_update_direction: PsoWindowUpdateDirection, execution_task_index: int = 1) -> None:
		'''
		Configures the array of window range pairs to update when exiting the active window range in specific directions.

		Args:
			axis: The axis on which to configure the window array update direction.
			window_number: The number of the window on which to configure the array update direction.
			window_update_direction: Mode selection to select the active window range exit directions on which to update the window range.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(window_number)
		argument_checking.validate_int_32(window_update_direction)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowConfigureArrayUpdateDirection(self.__capi_controller, execution_task_index, axis, window_number, window_update_direction))

	def psowindowconfigurecounterreset(self, axis: Union[int, str], options_mask: int, execution_task_index: int = 1) -> None:
		'''
		Configures the conditions which will reset the PSO window counters.

		Args:
			axis: The axis on which to configure the window counter reset conditions.
			options_mask: A bitmask of PSO window counter reset options. Use the values from the PsoWindowCounterResetMask enum.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(options_mask)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowConfigureCounterReset(self.__capi_controller, execution_task_index, axis, options_mask))

	def psowindowconfigureevents(self, axis: Union[int, str], event_mode: PsoWindowEventMode, execution_task_index: int = 1) -> None:
		'''
		Configures the conditions which will generate PSO window events.

		Args:
			axis: The axis on which to configure the window event conditions.
			event_mode: The specified window event mode.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_32(event_mode)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowConfigureEvents(self.__capi_controller, execution_task_index, axis, event_mode))

	def psowindowconfigurefixedrange(self, axis: Union[int, str], window_number: int, lower_bound: int, upper_bound: int, execution_task_index: int = 1) -> None:
		'''
		Configures a fixed window range consisting of a lower bound and an upper bound for the specified window.

		Args:
			axis: The axis on which to configure the window range.
			window_number: The number of the window on which to configure the range.
			lower_bound: The value for the window range lower bound.
			upper_bound: The value for the window range upper bound.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(window_number)
		argument_checking.validate_int_64(lower_bound)
		argument_checking.validate_int_64(upper_bound)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowConfigureFixedRange(self.__capi_controller, execution_task_index, axis, window_number, lower_bound, upper_bound))

	def psowindowconfigureinput(self, axis: Union[int, str], window_number: int, input: PsoWindowInput, reverse_direction: int, execution_task_index: int = 1) -> None:
		'''
		Selects the source of the specified window counter.

		Args:
			axis: The axis on which to select the window counter input source.
			window_number: The window number for which to select the counter input source.
			input: The window counter input source.
			reverse_direction: Configures the window counter to count in the opposite direction of its input source.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(window_number)
		argument_checking.validate_int_32(input)
		argument_checking.validate_int_64(reverse_direction)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowConfigureInput(self.__capi_controller, execution_task_index, axis, window_number, input, reverse_direction))

	def psowindowcountersetvalue(self, axis: Union[int, str], window_number: int, value: int, execution_task_index: int = 1) -> None:
		'''
		Sets the specified window counter to the specified value.

		Args:
			axis: The axis on which to set the window counter.
			window_number: The number of the window on which to set the counter.
			value: The new counter value.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(window_number)
		argument_checking.validate_int_64(value)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowCounterSetValue(self.__capi_controller, execution_task_index, axis, window_number, value))

	def psowindowoutputoff(self, axis: Union[int, str], window_number: int, execution_task_index: int = 1) -> None:
		'''
		Disables the specified window output.

		Args:
			axis: The axis on which to disable the window output.
			window_number: The number of the window on which to disable the output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(window_number)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowOutputOff(self.__capi_controller, execution_task_index, axis, window_number))

	def psowindowoutputon(self, axis: Union[int, str], window_number: int, execution_task_index: int = 1) -> None:
		'''
		Enables the specified window output.

		Args:
			axis: The axis on which to enable the window output.
			window_number: The number of the window on which to enable the output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(window_number)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PsoWindowOutputOn(self.__capi_controller, execution_task_index, axis, window_number))

	#endregion Methods

class IOCommands():
	'''
	A class to execute IO AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def analoginputget(self, axis: Union[int, str], input_num: int, execution_task_index: int = 1) -> float:
		'''
		Gets the value of a specified analog input.

		Args:
			axis: The axis on which to retrieve the value of the analog input.
			input_num: The number of the analog input to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified analog input.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(input_num)
		returnOut = ctypes.pointer(ctypes.c_double())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AnalogInputGet(self.__capi_controller, execution_task_index, axis, input_num, returnOut))
		return returnOut.contents.value

	def analogoutputconfigurearraymode(self, axis: Union[int, str], output_num: int, update_event: AnalogOutputUpdateEvent, drive_array_start_address: int, number_of_points: int, divisor: int, enable_repeat: int, execution_task_index: int = 1) -> None:
		'''
		Configures the specified analog output to use values from the drive array.

		Args:
			axis: The axis on which to apply the configuration.
			output_num: The number of the analog output to configure.
			update_event: The event which causes a new analog output value to be read from the drive array.
			drive_array_start_address: The byte-addressable index of the drive array where the first analog output value is stored.
			number_of_points: The number of analog output values to read from the drive array.
			divisor: Divides the default update event rate by the specified integer if $updateEvent is set to Time.
			enable_repeat: Configures the specified analog output to start over at the first analog output value after the last value in the drive array is used.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(output_num)
		argument_checking.validate_int_32(update_event)
		argument_checking.validate_int_64(drive_array_start_address)
		argument_checking.validate_int_64(number_of_points)
		argument_checking.validate_int_64(divisor)
		argument_checking.validate_int_64(enable_repeat)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AnalogOutputConfigureArrayMode(self.__capi_controller, execution_task_index, axis, output_num, update_event, drive_array_start_address, number_of_points, divisor, enable_repeat))

	def analogoutputconfigureaxistrackingmode(self, output_axis: Union[int, str], output_num: int, tracking_item: AnalogOutputAxisTrackingItem, scale_factor: float, offset: float, min_voltage: float, max_voltage: float, execution_task_index: int = 1) -> None:
		'''
		Configures an analog output to be dependent on a specified real-time internal servo loop value of a single axis.

		Args:
			output_axis: The axis of the servo loop value that $trackingItem is tracking.
			output_num: The index of the analog output to update.
			tracking_item: A servo loop value, such as position command, to track.
			scale_factor: The scale factor applied to the analog output.
			offset: This value is applied with the tracking value to the analog output. Use this argument if you want to track position on a stage where the position can never be negative. The units are volts.
			min_voltage: The minimum voltage that the analog output will be set to.
			max_voltage: The maximum voltage that the analog output will be set to.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		output_axis = AxisInput(output_axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(output_axis)
		argument_checking.validate_int_64(output_num)
		argument_checking.validate_int_32(tracking_item)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AnalogOutputConfigureAxisTrackingMode(self.__capi_controller, execution_task_index, output_axis, output_num, tracking_item, scale_factor, offset, min_voltage, max_voltage))

	def analogoutputconfiguredefaultmode(self, axis: Union[int, str], output_num: int, execution_task_index: int = 1) -> None:
		'''
		Restores the analog output configuration to the default operating mode.

		Args:
			axis: The axis on which to apply the configuration.
			output_num: The number of the analog output to configure.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(output_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AnalogOutputConfigureDefaultMode(self.__capi_controller, execution_task_index, axis, output_num))

	def analogoutputconfigurevectortrackingmode(self, output_axis: Union[int, str], output_num: int, input_axes: Union[int, str, Iterable[Union[int, str]]], tracking_item: AnalogOutputVectorTrackingItem, scale_factor: float, offset: float, min_voltage: float, max_voltage: float, execution_task_index: int = 1) -> None:
		'''
		Configures an analog output to be dependent on the square root of the sum of squares of a specified real-time internal servo loop value of multiple axes. The tracked value is always positive or zero.

		Args:
			output_axis: The axis of the servo loop value that $trackingItem is tracking.
			output_num: The index of the analog output to update.
			input_axes: A list of axes from which to read the $trackingItem from, vectorizing the result, in order to update the analog output.
			tracking_item: A servo loop value, such as position command, to track.
			scale_factor: The scale factor applied to the analog output.
			offset: This value is applied with the tracking value to the analog output. Use this argument if you want to track position on a stage where the position can never be negative. The units are volts.
			min_voltage: The minimum voltage that the analog output will be set to.
			max_voltage: The maximum voltage that the analog output will be set to.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		output_axis = AxisInput(output_axis).to_axis_index(self.__capi_controller)
		input_axes = AxisInputCollection(input_axes).to_axis_indices(self.__capi_controller)
		input_axes_c_array = c_helpers.create_c_array(ctypes.c_int32, input_axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(output_axis)
		argument_checking.validate_int_64(output_num)
		argument_checking.validate_int_32(input_axes)
		argument_checking.validate_int_32(tracking_item)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AnalogOutputConfigureVectorTrackingMode(self.__capi_controller, execution_task_index, output_axis, output_num, input_axes_c_array, len(input_axes), tracking_item, scale_factor, offset, min_voltage, max_voltage))

	def analogoutputget(self, axis: Union[int, str], output_num: int, execution_task_index: int = 1) -> float:
		'''
		Gets the value of a specified analog output.

		Args:
			axis: The axis on which to retrieve the value of the analog output.
			output_num: The number of the analog output to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified analog output.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(output_num)
		returnOut = ctypes.pointer(ctypes.c_double())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AnalogOutputGet(self.__capi_controller, execution_task_index, axis, output_num, returnOut))
		return returnOut.contents.value

	def analogoutputset(self, axis: Union[int, str], output_num: int, value: float, execution_task_index: int = 1) -> None:
		'''
		Sets the value of a specified analog output.

		Args:
			axis: The axis on which to set the value of the analog output.
			output_num: The number of the analog output to set.
			value: The value to set to the specified analog output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(output_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_AnalogOutputSet(self.__capi_controller, execution_task_index, axis, output_num, value))

	def digitalinputget(self, axis: Union[int, str], input_num: int, execution_task_index: int = 1) -> int:
		'''
		Gets the value of the specified digital input bit.

		Args:
			axis: The axis from which to get the digital input bit.
			input_num: The digital input bit to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified digital input bit.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(input_num)
		returnOut = ctypes.pointer(ctypes.c_int64())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DigitalInputGet(self.__capi_controller, execution_task_index, axis, input_num, returnOut))
		return returnOut.contents.value

	def digitaloutputget(self, axis: Union[int, str], output_num: int, execution_task_index: int = 1) -> int:
		'''
		Gets the value of the specified digital output bit.

		Args:
			axis: The axis from which to get the digital output bit.
			output_num: The digital output bit to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified digital output bit.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(output_num)
		returnOut = ctypes.pointer(ctypes.c_int64())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DigitalOutputGet(self.__capi_controller, execution_task_index, axis, output_num, returnOut))
		return returnOut.contents.value

	def digitaloutputset(self, axis: Union[int, str], output_num: int, value: int, execution_task_index: int = 1) -> None:
		'''
		Sets the value of the specified digital output bit.

		Args:
			axis: The axis on which to set the digital output bit.
			output_num: The digital output bit to set.
			value: The value of the specified digital output bit.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(output_num)
		argument_checking.validate_int_64(value)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_DigitalOutputSet(self.__capi_controller, execution_task_index, axis, output_num, value))

	def laseroutputset(self, axis: Union[int, str], laser_state: int, execution_task_index: int = 1) -> None:
		'''
		Sets the laser to manual mode and to the specified value.

		Args:
			axis: The axis on which to configure the laser state.
			laser_state: The value for the laser. To turn off the laser, specify a value of 0. To turn on the laser, specify a value of 1.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axis = AxisInput(axis).to_axis_index(self.__capi_controller)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axis)
		argument_checking.validate_int_64(laser_state)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_LaserOutputSet(self.__capi_controller, execution_task_index, axis, laser_state))

	def virtualbinaryinputget(self, input_num: int, execution_task_index: int = 1) -> int:
		'''
		Gets the value of the specified virtual binary input bit.

		Args:
			input_num: The virtual binary input bit to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified virtual binary input bit.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(input_num)
		returnOut = ctypes.pointer(ctypes.c_int64())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualBinaryInputGet(self.__capi_controller, execution_task_index, input_num, returnOut))
		return returnOut.contents.value

	def virtualbinaryinputset(self, input_num: int, value: int, execution_task_index: int = 1) -> None:
		'''
		Sets the value of the specified virtual binary input bit.

		Args:
			input_num: The virtual binary input bit to set.
			value: The value to which you set the virtual binary input bit.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(input_num)
		argument_checking.validate_int_64(value)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualBinaryInputSet(self.__capi_controller, execution_task_index, input_num, value))

	def virtualbinaryoutputget(self, output_num: int, execution_task_index: int = 1) -> int:
		'''
		Gets the value of the specified virtual binary output bit.

		Args:
			output_num: The virtual binary output bit to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified virtual binary output bit.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(output_num)
		returnOut = ctypes.pointer(ctypes.c_int64())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualBinaryOutputGet(self.__capi_controller, execution_task_index, output_num, returnOut))
		return returnOut.contents.value

	def virtualbinaryoutputset(self, output_num: int, value: int, execution_task_index: int = 1) -> None:
		'''
		Sets the value of the specified virtual binary output bit.

		Args:
			output_num: The virtual binary output bit to set.
			value: The value to which you set the virtual binary output bit.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(output_num)
		argument_checking.validate_int_64(value)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualBinaryOutputSet(self.__capi_controller, execution_task_index, output_num, value))

	def virtualregisterinputget(self, input_num: int, execution_task_index: int = 1) -> float:
		'''
		Gets the value of a specified virtual register input.

		Args:
			input_num: The number of the virtual register input to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified virtual register input.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(input_num)
		returnOut = ctypes.pointer(ctypes.c_double())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualRegisterInputGet(self.__capi_controller, execution_task_index, input_num, returnOut))
		return returnOut.contents.value

	def virtualregisterinputset(self, input_num: int, value: float, execution_task_index: int = 1) -> None:
		'''
		Sets the value of a specified virtual register input.

		Args:
			input_num: The number of the virtual register input to set.
			value: The value to set to the virtual register input.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(input_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualRegisterInputSet(self.__capi_controller, execution_task_index, input_num, value))

	def virtualregisteroutputget(self, output_num: int, execution_task_index: int = 1) -> float:
		'''
		Gets the value of a specified virtual register output.

		Args:
			output_num: The number of the virtual register output to get.
			execution_task_index: The index of the task to execute the AeroScript command on.

		Returns:
			The value of the specified virtual register output.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(output_num)
		returnOut = ctypes.pointer(ctypes.c_double())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualRegisterOutputGet(self.__capi_controller, execution_task_index, output_num, returnOut))
		return returnOut.contents.value

	def virtualregisteroutputset(self, output_num: int, value: float, execution_task_index: int = 1) -> None:
		'''
		Sets the value of a specified virtual register output.

		Args:
			output_num: The number of the virtual register output to set.
			value: The value to set to the virtual register output.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(output_num)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_VirtualRegisterOutputSet(self.__capi_controller, execution_task_index, output_num, value))

	#endregion Methods

class MotionCommands():
	'''
	A class to execute Motion AeroScript commands on the Automation1 controller. Access an instance of this class through a Controller object instance.
	'''

	#region Constructor

	def __init__(self, controller: ctypes.c_void_p) -> None:
		'''
		Constructor
		'''
		self.__capi_controller = controller

	#endregion Constructor

	#region Methods

	def abort(self, axes: Union[int, str, Iterable[Union[int, str]]]) -> None:
		'''
		Aborts motion on the specified axes. The controller stops all motion and ramps the axes to zero speed.
		This method waits for the abort to start but it does not wait for the abort to complete.
		This function does not block. It is different from the AeroScript Abort() function, which does block.
		Use the waitformotiondone() method to ensure aborted motion is done before executing the next command,
		otherwise an error might occur.

		Args:
			axes: The axes to abort.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_Abort(self.__capi_controller, axes_c_array, len(axes)))
		
	def disable(self, axes: Union[int, str, Iterable[Union[int, str]]]) -> None:
		'''
		Disables the axes so that you cannot command motion.
		This method waits for the disable to start but it does not wait for the disable to complete.
		This function does not block. It is different from the AeroScript Disable() function, which does block.

		Args:
			axes: The axes to disable.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_Disable(self.__capi_controller, axes_c_array, len(axes)))

	def enable(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Enables the axes so that you can command motion.

		Args:
			axes: The axes to enable.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_Enable(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def home(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Performs a home cycle by moving the axes to a known hardware reference location. The task waits for completion of the home cycle.

		Args:
			axes: The axes to home.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_Home(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def homeasync(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Performs a home cycle by moving the axes to a known hardware reference location. The controller performs the home cycle asynchronously so that the task moves on without waiting for completion.

		Args:
			axes: The axes to home.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_HomeAsync(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def moveabsolute(self, axes: Union[int, str, Iterable[Union[int, str]]], positions: List[float], speeds: List[float], execution_task_index: int = 1) -> None:
		'''
		Executes an asynchronous point-to-point move to an absolute target-position on the specified axes.

		Args:
			axes: The axes on which to perform point-to-point motion.
			positions: The absolute target-positions of the move.
			speeds: The speeds at which to move the specified axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		positions_c_array = c_helpers.create_c_array(ctypes.c_double, positions)
		speeds_c_array = c_helpers.create_c_array(ctypes.c_double, speeds)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveAbsolute(self.__capi_controller, execution_task_index, axes_c_array, len(axes), positions_c_array, len(positions), speeds_c_array, len(speeds)))

	def moveccwbyradius(self, axes: Union[int, str, Iterable[Union[int, str]]], distances: List[float], radius: float, coordinated_speed: float, execution_task_index: int = 1) -> None:
		'''
		Executes a coordinated counterclockwise circular arc move on the specified axes. An arc move creates an arc in vector space using two axes.

		Args:
			axes: The axes on which to perform counterclockwise circular motion.
			distances: The end points of the circular arc.
			radius: The radius of the circular arc.
			coordinated_speed: The speed of the coordinated circular motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		distances_c_array = c_helpers.create_c_array(ctypes.c_double, distances)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveCcwByRadius(self.__capi_controller, execution_task_index, axes_c_array, len(axes), distances_c_array, len(distances), radius, coordinated_speed))

	def moveccwbycenter(self, axes: Union[int, str, Iterable[Union[int, str]]], distances: List[float], center: List[float], coordinated_speed: float, execution_task_index: int = 1) -> None:
		'''
		Executes a coordinated counterclockwise circular arc move on the specified axes. An arc move creates an arc in vector space using two axes.

		Args:
			axes: The axes on which to perform counterclockwise circular motion.
			distances: The end points of the circular arc.
			center: The relative offsets of the center point from the starting positions of the axes.
			coordinated_speed: The speed of the coordinated circular motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		distances_c_array = c_helpers.create_c_array(ctypes.c_double, distances)
		center_c_array = c_helpers.create_c_array(ctypes.c_double, center)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveCcwByCenter(self.__capi_controller, execution_task_index, axes_c_array, len(axes), distances_c_array, len(distances), center_c_array, len(center), coordinated_speed))

	def movecwbyradius(self, axes: Union[int, str, Iterable[Union[int, str]]], distances: List[float], radius: float, coordinated_speed: float, execution_task_index: int = 1) -> None:
		'''
		Executes a coordinated clockwise circular arc move on the specified axes. An arc move creates an arc in vector space using two axes.

		Args:
			axes: The axes on which to perform clockwise circular motion.
			distances: The end points of the circular arc.
			radius: The radius of the circular arc.
			coordinated_speed: The speed of the coordinated circular motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		distances_c_array = c_helpers.create_c_array(ctypes.c_double, distances)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveCwByRadius(self.__capi_controller, execution_task_index, axes_c_array, len(axes), distances_c_array, len(distances), radius, coordinated_speed))

	def movecwbycenter(self, axes: Union[int, str, Iterable[Union[int, str]]], distances: List[float], center: List[float], coordinated_speed: float, execution_task_index: int = 1) -> None:
		'''
		Executes a coordinated clockwise circular arc move on the specified axes. An arc move creates an arc in vector space using two axes.

		Args:
			axes: The axes on which to perform clockwise circular motion.
			distances: The end points of the circular arc.
			center: The relative offsets of the center point from the starting positions of the axes.
			coordinated_speed: The speed of the coordinated circular motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		distances_c_array = c_helpers.create_c_array(ctypes.c_double, distances)
		center_c_array = c_helpers.create_c_array(ctypes.c_double, center)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveCwByCenter(self.__capi_controller, execution_task_index, axes_c_array, len(axes), distances_c_array, len(distances), center_c_array, len(center), coordinated_speed))

	def movedelay(self, axes: Union[int, str, Iterable[Union[int, str]]], delay_time: float, execution_task_index: int = 1) -> None:
		'''
		Commands axes to remain at zero velocity for a quantity of time.

		Args:
			axes: The axes on which to perform the delay.
			delay_time: Total delay time in milliseconds, rounded to the nearest time interval of the MotionUpdateRate parameter.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveDelay(self.__capi_controller, execution_task_index, axes_c_array, len(axes), delay_time))

	def movefreerun(self, axes: Union[int, str, Iterable[Union[int, str]]], velocities: List[float], execution_task_index: int = 1) -> None:
		'''
		Executes an asynchronous freerun move on the specified axes. The axes will move indefinitely at the specified velocity.

		Args:
			axes: The axes on which to perform freerun motion.
			velocities: The velocities at which to move the specified axes. The signs of the velocities specify the directions of motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		velocities_c_array = c_helpers.create_c_array(ctypes.c_double, velocities)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveFreerun(self.__capi_controller, execution_task_index, axes_c_array, len(axes), velocities_c_array, len(velocities)))

	def movefreerunstop(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Stops an asynchronous freerun move on the specified axes. The axis velocities decelerate to zero.

		Args:
			axes: The axes on which to stop freerun motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveFreerunStop(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def moveincremental(self, axes: Union[int, str, Iterable[Union[int, str]]], distances: List[float], speeds: List[float], execution_task_index: int = 1) -> None:
		'''
		Executes an asynchronous point-to-point move by an incremental distance on the specified axes.

		Args:
			axes: The axes on which to perform point-to-point motion.
			distances: The distances and directions to move the specified axes relative to the current positions. A distance of zero results in no motion.
			speeds: The speeds at which to move the specified axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		distances_c_array = c_helpers.create_c_array(ctypes.c_double, distances)
		speeds_c_array = c_helpers.create_c_array(ctypes.c_double, speeds)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveIncremental(self.__capi_controller, execution_task_index, axes_c_array, len(axes), distances_c_array, len(distances), speeds_c_array, len(speeds)))

	def movelinear(self, axes: Union[int, str, Iterable[Union[int, str]]], distances: List[float], coordinated_speed: float, execution_task_index: int = 1) -> None:
		'''
		Executes a coordinated linear move on the specified axes. A linear move creates a line in vector space on one or more axes.

		Args:
			axes: The axes on which to perform linear motion.
			distances: The end points of the linear move.
			coordinated_speed: The speed of the coordinated linear motion.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		distances_c_array = c_helpers.create_c_array(ctypes.c_double, distances)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveLinear(self.__capi_controller, execution_task_index, axes_c_array, len(axes), distances_c_array, len(distances), coordinated_speed))

	def moverapid(self, axes: Union[int, str, Iterable[Union[int, str]]], distances: List[float], speeds: List[float], execution_task_index: int = 1) -> None:
		'''
		Executes a point-to-point rapid move on the specified axes.

		Args:
			axes: The axes on which to perform point-to-point rapid motion.
			distances: The end points of the rapid move.
			speeds: The speeds at which to move each of the axes.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		distances_c_array = c_helpers.create_c_array(ctypes.c_double, distances)
		speeds_c_array = c_helpers.create_c_array(ctypes.c_double, speeds)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_MoveRapid(self.__capi_controller, execution_task_index, axes_c_array, len(axes), distances_c_array, len(distances), speeds_c_array, len(speeds)))

	def positionoffsetclear(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Clears the program position offsets on the specified axes. The program positions will be restored to the current axis positions.

		Args:
			axes: The axes on which to clear the program position offsets.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PositionOffsetClear(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def positionoffsetset(self, axes: Union[int, str, Iterable[Union[int, str]]], program_positions: List[float], execution_task_index: int = 1) -> None:
		'''
		Sets the program positions of the specified axes to the specified values. The controller applies an offset to the current axis positions so that the axes do not move. All moves that specify an absolute target-position will be relative to the new program position.

		Args:
			axes: The axes on which to set the program positions.
			program_positions: The new program positions to set.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		program_positions_c_array = c_helpers.create_c_array(ctypes.c_double, program_positions)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_PositionOffsetSet(self.__capi_controller, execution_task_index, axes_c_array, len(axes), program_positions_c_array, len(program_positions)))

	def waitforinposition(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Waits for motion to be done on the specified axes and for the axes to be in position. The motion is done when the commanded velocity is at zero. The axes are in position when the position error is at the threshold specified by the InPositionTime and InPositionDistance parameters.

		Args:
			axes: The axes on which to wait for motion to be done and in position.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_WaitForInPosition(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def waitformotiondone(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Waits for motion to be done on the specified axes. The motion is done when the commanded velocity is at zero.

		Args:
			axes: The axes on which to wait for motion to be done.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_WaitForMotionDone(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def workoffsetconfigureoffset(self, offset_number: int, axes: Union[int, str, Iterable[Union[int, str]]], program_positions: List[float], execution_task_index: int = 1) -> None:
		'''
		Configures the specified work offset on the specified axes and values. Previously configured axes will retain their values unless overwritten.

		Args:
			offset_number: The index of the work offset to configure. An integer between and including 1 and 100.
			axes: The axes on which to configure work offset values.
			program_positions: The program positions to set as the work offset origin.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		program_positions_c_array = c_helpers.create_c_array(ctypes.c_double, program_positions)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(offset_number)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_WorkOffsetConfigureOffset(self.__capi_controller, execution_task_index, offset_number, axes_c_array, len(axes), program_positions_c_array, len(program_positions)))

	def workoffsetdisable(self, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Deactivates work offsets for all axes on the controller.

		Args:
			axes: The axes on which to disable work offsets.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_WorkOffsetDisable(self.__capi_controller, execution_task_index, axes_c_array, len(axes)))

	def workoffsetenable(self, offset_number: int, axes: Union[int, str, Iterable[Union[int, str]]], execution_task_index: int = 1) -> None:
		'''
		Activates the specified work offset and applies offsets to the specified axes.

		Args:
			offset_number: The index of the work offset to enable. An integer between and including 1 and 100.
			axes: The axes on which to enable the specified work offset.
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		axes = AxisInputCollection(axes).to_axis_indices(self.__capi_controller)
		axes_c_array = c_helpers.create_c_array(ctypes.c_int32, axes)
		argument_checking.validate_int_32(execution_task_index)
		argument_checking.validate_int_64(offset_number)
		argument_checking.validate_int_32(axes)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_WorkOffsetEnable(self.__capi_controller, execution_task_index, offset_number, axes_c_array, len(axes)))

	def workoffsetresetconfiguration(self, execution_task_index: int = 1) -> None:
		'''
		Erases the work offset configurations on all axes. All work offsets must first be disabled.

		Args:
			execution_task_index: The index of the task to execute the AeroScript command on.
		'''
		argument_checking.validate_int_32(execution_task_index)
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_Command_WorkOffsetResetConfiguration(self.__capi_controller, execution_task_index))

	#endregion Methods


