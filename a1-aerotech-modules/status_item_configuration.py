from automation1.public.status.status_items_gen import AxisStatusItem, TaskStatusItem, SystemStatusItem
from automation1.internal.axis_input import AxisInput
from automation1.internal.task_input import TaskInput
from typing import Set, Tuple, Union

class StatusItemConfiguration():
	'''
	Represents a configuration of status items to retrieve from an Automation1 controller using the status.get_status_items method
	via the ControllerRuntime.status property. Add status items to retrieve using the system, axis, and task properties.
	'''

	#region Constructor

	def __init__(self) -> None:
		'''
		Constructs a new, empty StatusItemConfiguration. Add status items to retrieve using the system, axis, and task properties.
		'''
		self.__axis = AxisStatusItemConfigurationCollection()
		self.__task = TaskStatusItemConfigurationCollection()
		self.__system = SystemStatusItemConfigurationCollection()
		self.__industrial_ethernet = IndustrialEthernetStatusItemConfigurationCollection()

	#endregion Constructor

	#region Properties

	@property
	def axis(self) -> 'AxisStatusItemConfigurationCollection':
		'''
		Gets the configuration of axis based status items to retrieve from an Automation1 controller.
		'''
		return self.__axis

	@property
	def task(self) -> 'TaskStatusItemConfigurationCollection':
		'''
		Gets the configuration of task based status items to retrieve from an Automation1 controller.
		'''
		return self.__task

	@property
	def system(self) -> 'SystemStatusItemConfigurationCollection':
		'''
		Gets the configuration of system based status items to retrieve from an Automation1 controller.
		'''
		return self.__system
	
	@property
	def industrial_ethernet(self) -> 'IndustrialEthernetStatusItemConfigurationCollection':
		'''
		Gets the configuration of Industrial Ethernet mappings to retrieve from an Automation1 controller.
		'''
		return self.__industrial_ethernet

	@property
	def count(self) -> int:
		'''
		Gets the total number of all status items added to this configuration to be retrieved from an Automation1 controller.
		'''
		return self.__axis.count + self.__task.count + self.__system.count + self.__industrial_ethernet.count

	#endregion Properties

	#region Methods

	def add_from(self, other_status_item_configuration: 'StatusItemConfiguration'):
		'''
		Adds all configured status items from another StatusItemConfiguration to this configuration.
		This will update the Axis, Task, and System configurations.

		Args:
			other_status_item_configuration: The other StatusItemConfiguration to add status items from.
		'''
		self.axis.add_from(other_status_item_configuration.axis)
		self.task.add_from(other_status_item_configuration.task)
		self.system.add_from(other_status_item_configuration.system)
		self.industrial_ethernet.add_from(other_status_item_configuration.industrial_ethernet)

	def clear(self):
		'''
		Removes all status items from this configuration so they will not be retrieved from the Automation1 controller.
		'''
		self.axis.clear()
		self.task.clear()
		self.system.clear()
		self.industrial_ethernet.clear()

	#endregion Methods

class AxisStatusItemConfigurationCollection():
	'''
	Represents a collection of configured axis based status items to retrieve from an Automation1 controller.
	Use the AxisStatusItemConfigurationCollection.add and AxisStatusItemConfigurationCollection.remove methods to 
	control what axis based status items to retrieve.
	'''

	#region Constructor

	def __init__(self) -> None:
		'''
		Constructor
		'''
		self.__configured_status_items = set()

	#endregion Constructor

	#region Properties

	@property
	def _configured_status_items(self) -> Set[Tuple[AxisStatusItem, AxisInput, int]]:
		'''
		Gets the internal collection of user configured axis based status items.
		'''
		return self.__configured_status_items.copy()

	@property
	def count(self) -> int:
		'''
		Gets the number of axis based status items added to this configuration to be retrieved from an Automation1 controller.
		'''
		return len(self.__configured_status_items)

	#endregion Properties

	#region Methods

	def add_from(self, other_axis_status_item_configuration: 'AxisStatusItemConfigurationCollection'):
		'''
		Adds all configured axis based status items from another AxisStatusItemConfigurationCollection to this configuration.

		Args:
			other_axis_status_item_configuration: The other AxisStatusItemConfigurationCollection to add status items from.
		'''
		self.__configured_status_items = self.__configured_status_items.union(other_axis_status_item_configuration.__configured_status_items)

	def add(self, axis_status_item: AxisStatusItem, axis: Union[int, str], argument: int = 0):
		'''
		Adds an axis based status item to be retrieved on a specific axis on the Automation1 controller, with an
		optional argument for the status item.

		Args:
			axis_status_item: The axis based status item to retrieve.
			axis: The axis to retrieve the status item on.
			argument: The argument for the status item, if unsure don't pass anything for this argument.
		'''
		self.__configured_status_items.add((axis_status_item, AxisInput(axis), argument))

	def remove(self, axis_status_item: AxisStatusItem, axis: Union[int, str], argument: int = 0):
		'''
		Removes an axis based status item from this configuration so it will not be retrieved from the Automation1 controller.
		
		Args:
			axis_status_item: The axis based status item to remove.
			axis: The axis that the status item was to be retrieved on.
			argument: The argument for the status item, if unsure don't pass anything for this argument.
		'''
		self.__configured_status_items.remove((axis_status_item, AxisInput(axis), argument))
		
	def clear(self):
		'''
		Removes all axis based status items from this configuration so they will not be retrieved from the Automation1 controller.
		'''
		self.__configured_status_items.clear()

	#endregion Methods

class TaskStatusItemConfigurationCollection():
	'''
	Represents a collection of configured task based status items to retrieve from an Automation1 controller.
	Use the TaskStatusItemConfigurationCollection.add and TaskStatusItemConfigurationCollection.remove methods to 
	control what task based status items to retrieve.
	'''

	#region Constructor

	def __init__(self) -> None:
		'''
		Constructor
		'''
		self.__configured_status_items = set()

	#endregion Constructor

	#region Properties

	@property
	def _configured_status_items(self) -> Set[Tuple[TaskStatusItem, TaskInput, int]]:
		'''
		Gets the internal collection of user configured task based status items.
		'''
		return self.__configured_status_items.copy()

	@property
	def count(self) -> int:
		'''
		Gets the number of task based status items added to this configuration to be retrieved from an Automation1 controller.
		'''
		return len(self.__configured_status_items)

	#endregion Properties

	#region Methods

	def add_from(self, other_task_status_item_configuration: 'TaskStatusItemConfigurationCollection'):
		'''
		Adds all configured task based status items from another TaskStatusItemConfigurationCollection to this configuration.

		Args:
			other_task_status_item_configuration: The other TaskStatusItemConfigurationCollection to add status items from.
		'''
		self.__configured_status_items = self.__configured_status_items.union(other_task_status_item_configuration.__configured_status_items)

	def add(self, task_status_item: TaskStatusItem, task: Union[int, str], argument: int = 0):
		'''
		Adds an task based status item to be retrieved on a specific task on the Automation1 controller, with an
		optional argument for the status item.

		Args:
			task_status_item: The task based status item to retrieve.
			task: The task to retrieve the status item on.
			argument: The argument for the status item, if unsure don't pass anything for this argument.
		'''
		self.__configured_status_items.add((task_status_item, TaskInput(task), argument))

	def remove(self, task_status_item: TaskStatusItem, task: Union[int, str], argument: int = 0):
		'''
		Removes an task based status item from this configuration so it will not be retrieved from the Automation1 controller.
		
		Args:
			task_status_item: The task based status item to remove.
			task: The task that the status item was to be retrieved on.
			argument: The argument for the status item, if unsure don't pass anything for this argument.
		'''
		self.__configured_status_items.remove((task_status_item, TaskInput(task), argument))
		
	def clear(self):
		'''
		Removes all task based status items from this configuration so they will not be retrieved from the Automation1 controller.
		'''
		self.__configured_status_items.clear()

	#endregion Methods

class SystemStatusItemConfigurationCollection():
	'''
	Represents a collection of configured system based status items to retrieve from an Automation1 controller.
	Use the SystemStatusItemConfigurationCollection.add and SystemStatusItemConfigurationCollection.remove methods to control what system based status items to retrieve.
	'''

	#region Constructor

	def __init__(self) -> None:
		'''
		Constructor
		'''
		self.__configured_status_items = set()

	#endregion Constructor

	#region Properties

	@property
	def _configured_status_items(self) -> Set[Tuple[SystemStatusItem, int]]:
		'''
		Gets the internal collection of user configured system based status items.
		'''
		return self.__configured_status_items.copy()

	@property
	def count(self) -> int:
		'''
		Gets the number of system based status items added to this configuration to be retrieved from an Automation1 controller.
		'''
		return len(self.__configured_status_items)

	#endregion Properties

	#region Methods

	def add_from(self, other_system_status_item_configuration: 'SystemStatusItemConfigurationCollection'):
		'''
		Adds all configured system based status items from another SystemStatusItemConfigurationCollection to this configuration.

		Args:
			other_system_status_item_configuration: The other SystemStatusItemConfigurationCollection to add status items from.
		'''
		self.__configured_status_items = self.__configured_status_items.union(other_system_status_item_configuration.__configured_status_items)

	def add(self, system_status_item: SystemStatusItem, argument: int = 0):
		'''
		Adds a system based status item to be retrieved from the Automation1 controller, with an
		optional argument for the status item.

		Args:
			system_status_item: The system based status item to retrieve.
			argument: The argument for the status item, if unsure don't pass anything for this argument.
		'''
		self.__configured_status_items.add((system_status_item, argument))

	def remove(self, system_status_item: SystemStatusItem, argument: int = 0):
		'''
		Removes an system based status item from this configuration so it will not be retrieved from the Automation1 controller.
		
		Args:
			system_status_item: The system based status item to remove.
			argument: The argument for the status item, if unsure don't pass anything for this argument.
		'''
		self.__configured_status_items.remove((system_status_item, argument))
		
	def clear(self):
		'''
		Removes all system based status items from this configuration so they will not be retrieved from the Automation1 controller.
		'''
		self.__configured_status_items.clear()

	#endregion Methods

class IndustrialEthernetStatusItemConfigurationCollection():
	'''
	Represents a collection of configured Industrial Ethernet mappings to retrieve from an Automation1 controller.
	Use the IndustrialEthernetStatusItemConfigurationCollection.add and IndustrialEthernetStatusItemConfigurationCollection.remove methods to control what Industrial Ethernet mappings to retrieve.
	'''

	#region Constructor

	def __init__(self) -> None:
		'''
		Constructor
		'''
		self.__configured_status_items = set()

	#endregion Constructor

	#region Properties

	@property
	def _configured_status_items(self) -> Set[Tuple[str, int]]:
		'''
		Gets the internal collection of user configured Industrial Ethernet mappings.
		'''
		return self.__configured_status_items.copy()

	@property
	def count(self) -> int:
		'''
		Gets the number of Industrial Ethernet mappings added to this configuration to be retrieved from an Automation1 controller.
		'''
		return len(self.__configured_status_items)

	#endregion Properties

	#region Methods

	def add_from(self, other_industrial_ethernet_status_item_configuration: 'IndustrialEthernetStatusItemConfigurationCollection') -> None:
		'''
		Adds all configured Industrial Ethernet mappings from another SystemStatusItemConfigurationCollection to this configuration.

		Args:
			other_industrial_ethernet_status_item_configuration: The other IndustrialEthernetStatusItemConfigurationCollection to add status items from.
		'''
		self.__configured_status_items = self.__configured_status_items.union(other_industrial_ethernet_status_item_configuration.__configured_status_items)

	def add(self, industrial_ethernet_mapping_name: str, industrial_ethernet_mapping_array_index: int = -1) -> None:
		'''
		Adds an Industrial Ethernet mapping to be retrieved from the Automation1 controller.

		Args:
			industrial_ethernet_mapping_name: The Industrial Ethernet mapping to retrieve.
			industrial_ethernet_mapping_array_index: The index of the Industrial Ethernet mapping array. If the specified Industrial Ethernet mapping is not an array, set this to -1.
		'''
		industrial_ethernet_mapping_name = industrial_ethernet_mapping_name[1:] if industrial_ethernet_mapping_name.startswith("$") else industrial_ethernet_mapping_name
		self.__configured_status_items.add((industrial_ethernet_mapping_name, industrial_ethernet_mapping_array_index))

	def remove(self, industrial_ethernet_mapping_name: str, industrial_ethernet_mapping_array_index: int = -1) -> None:
		'''
		Removes an Industrial Ethernet mapping from this configuration so it will not be retrieved from the Automation1 controller.
		
		Args:
			industrial_ethernet_mapping_name: The Industrial Ethernet mapping to remove.
			industrial_ethernet_mapping_array_index: The index of the Industrial Ethernet mapping array. If the specified Industrial Ethernet mapping is not an array, set this to -1.
		'''
		industrial_ethernet_mapping_name = industrial_ethernet_mapping_name[1:] if industrial_ethernet_mapping_name.startswith("$") else industrial_ethernet_mapping_name
		self.__configured_status_items.remove((industrial_ethernet_mapping_name, industrial_ethernet_mapping_array_index))
		
	def clear(self) -> None:
		'''
		Removes all Industrial Ethernet mappings from this configuration so they will not be retrieved from the Automation1 controller.
		'''
		self.__configured_status_items.clear()

	#endregion Methods
