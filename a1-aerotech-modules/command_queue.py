import ctypes
import automation1.internal.capi_error_handler as capi_error_handler
import automation1.internal.capi_wrapper as capi_wrapper
import automation1.internal.exception_resolver_gen as exception_resolver
from automation1.public.command_queue.command_queue_commands_gen import CommandQueueCommands
from automation1.public.command_queue.command_queue_status import CommandQueueStatus, CApiCommandQueueStatus

class CommandQueue:
	'''
	Represents a command queue on a specific task on an Automation1 controller. This class lets you manage and add commands to the command queue.
	Use the Commands.begin_command_queue() method to begin a command queue on a specific task.
	When you are done with the command queue, use the Commands.end_command_queue() method to end the command queue and return the task to its normal state.
	A command queue on a task will store all AeroScript commands added to the command queue and execute them sequentially, in the order they were added.
	Adding AeroScript commands to the command queue does not block (unless the command queue is full and should_block_if_full is True), instead the AeroScript command is added to the command queue and will be executed in the future once all previously added commands are executed.
	A command queue is usually used to avoid the communication latency in between AeroScript commands when executing your motion with the Commands API (such as when using velocity blending where the communication latency will cause deceleration to occur).
	A task can only execute queued commands while the command queue is active; non-queued commands from the Commands API and AeroScript programs cannot run while the command queue is active.
	'''

	#region Constructor

	def __init__(self, capi_controller: ctypes.c_void_p, capi_command_queue: ctypes.c_void_p, task_index: int, task_name: str, command_capacity: int, should_block_if_full: bool) -> None:
		'''
		Constructor.
		'''
		self.__capi_controller = capi_controller
		self._capi_command_queue = capi_command_queue
		self.__commands = CommandQueueCommands(self.__capi_controller, self._capi_command_queue)
		self.__task_index = task_index
		self.__task_name = task_name
		self.__command_capacity = command_capacity
		self.__should_block_if_full = should_block_if_full

	#endregion Constructor

	#region Properties

	@property
	def commands(self) -> CommandQueueCommands:
		'''
		Gets a way to add commands to the command queue.
		'''	
		return self.__commands

	@property
	def task_index(self) -> int:
		'''
		Gets the numeric index of the task that this command queue exists on.
		'''
		return self.__task_index

	@property
	def task_name(self) -> str:
		'''
		Gets the name of the task that this command queue exists on.
		This will be an empty string if a task index is supplied when creating the command queue.
		'''
		return self.__task_name

	@property
	def command_capacity(self) -> int:
		'''
		Gets the maximum number of unexecuted AeroScript commands that can be stored in this command queue, after which the command queue is full.
		'''
		return self.__command_capacity

	@property
	def should_block_if_full(self) -> bool:
		'''
		Gets whether or not to block if you add an AeroScript command when this command queue is full.
		If True, the add will block until the command can be added. If False, a ControllerOperationException will be raised.
		'''
		return self.__should_block_if_full
	
	@property
	def status(self) -> CommandQueueStatus:
		'''
		Gets the current status of this command queue.
		'''
		if self._capi_command_queue.value == None:
			raise exception_resolver.OperationException_API_CommandQueueEnded()

		capi_status_pointer = ctypes.pointer(CApiCommandQueueStatus())
		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_CommandQueue_GetStatus(self._capi_command_queue, capi_status_pointer))
		status = CommandQueueStatus(capi_status_pointer.contents)
		return status

	#endregion Properties
	
	#region Methods

	def wait_for_empty(self, milliseconds_timeout: int = -1) -> None:
		'''
		Waits for the command queue to be empty, blocking until all AeroScript commands added to the command queue have been executed.
		You can use this method to make sure the command queue is no longer executing commands before ending it with Commands.end_command_queue().

		Args:
			milliseconds_timeout: The number of milliseconds to wait for the command queue to be empty.
				If the command queue takes longer than this amount of time to be empty, a ControllerOperationException will be raised.
				This function will wait indefinitely for the command queue to be empty if this value is set to - 1.
		'''
		if self._capi_command_queue.value == None:
			raise exception_resolver.OperationException_API_CommandQueueEnded()

		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_CommandQueue_WaitForEmpty(self._capi_command_queue, milliseconds_timeout))

	def resume(self) -> None:
		'''
		Resumes the execution of queued AeroScript commands from a command queue.
		'''
		if self._capi_command_queue.value == None:
			raise exception_resolver.OperationException_API_CommandQueueEnded()

		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_CommandQueue_Resume(self._capi_command_queue))

	def pause(self) -> None:
		'''
		Pauses the execution of queued AeroScript commands from a command queue. 
		The currently executing AeroScript command, if any, will complete normally; the command will not be aborted.
		'''
		if self._capi_command_queue.value == None:
			raise exception_resolver.OperationException_API_CommandQueueEnded()

		capi_error_handler.call_function(lambda: capi_wrapper.capi.Automation1_CommandQueue_Pause(self._capi_command_queue))

	#endregion Methods
