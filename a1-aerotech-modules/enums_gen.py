from automation1.internal.cenum import CEnum

class DistanceUnits(CEnum):
	'''
	Represents the type of distance units used for motion.
	'''
	_init_ = 'value __doc__',
	Primary = 0,
	'''
	Primary units.
	'''
	Secondary = 1,
	'''
	Secondary units.
	'''

class TimeUnits(CEnum):
	'''
	Represents the type of time units used for motion.
	'''
	_init_ = 'value __doc__',
	Seconds = 0,
	'''
	Feedrates are specified in distance units per second.
	'''
	Minutes = 1,
	'''
	Feedrates are specified in distance units per minute.
	'''

class TargetMode(CEnum):
	'''
	Represents a motion target mode.
	'''
	_init_ = 'value __doc__',
	Incremental = 0,
	'''
	Motion target positions are relative to the current axis locations.
	'''
	Absolute = 1,
	'''
	Motion target positions are absolute.
	'''

class WaitMode(CEnum):
	'''
	Represents a motion waiting mode.
	'''
	_init_ = 'value __doc__',
	MotionDone = 1,
	'''
	Wait for the motion to be done before continuing execution.
	'''
	InPosition = 2,
	'''
	Wait for the motion to be done and for the position error to reach a specified value before continuing execution.
	'''
	Auto = 3,
	'''
	Wait the minimum quantity of time between motion blocks before continuing execution.
	'''

class NormalcyAlignment(CEnum):
	'''
	Represents the type of normalcy alignment.
	'''
	_init_ = 'value __doc__',
	Left = 0,
	'''
	Keeps the normalcy axis perpendicular and to the left of the part.
	'''
	Right = 1,
	'''
	Keeps the normalcy axis perpendicular and to the right of the part.
	'''
	Relative = 2,
	'''
	Keeps the normalcy axis at a relative angle to the part.
	'''

class IndicatorAnimationType(CEnum):
	'''
	Represents the animation type of an App Indicator.
	'''
	_init_ = 'value __doc__',
	Solid = 0,
	'''
	Solid background using $backgroundColor1 and $foregroundColor1.
	'''
	Flash = 1,
	'''
	Flashes between $backgroundColor1 and transparent with no transition colors between the two. The foreground color is $foregroundColor1 for the full animation.
	'''
	TwoColorFlash = 2,
	'''
	Flashes between $backgroundColor1 and $backgroundColor2 with no transition colors between the two. Also alternates the $displayText between $foregroundColor1 and $foregroundColor2.
	'''
	ColorSweep = 3,
	'''
	Transitions smoothly between $backgroundColor1 and $backgroundColor2 with intermediary colors. Also transitions the $displayText between $foregroundColor1 and $foregroundColor2.
	'''

class GalvoLaser(CEnum):
	'''
	Represents the mode for controlling a laser.
	'''
	_init_ = 'value __doc__',
	Off = 0,
	'''
	Manually turns off the laser.
	'''
	On = 1,
	'''
	Manually turns on the laser.
	'''
	Auto = 2,
	'''
	Specifies that the laser is automatically controlled.
	'''

class GalvoWobbleMode(CEnum):
	'''
	Specifies the mode of the wobble pattern.
	'''
	_init_ = 'value __doc__',
	TimeBased = 0,
	'''
	The wobble is repeated at a fixed time interval.
	'''
	DistanceBased = 1,
	'''
	The wobble is repeated at a fixed vector distance.
	'''

class GalvoWobbleType(CEnum):
	'''
	Specifies the type of the wobble pattern.
	'''
	_init_ = 'value __doc__',
	Ellipse = 0,
	'''
	The pattern uses an ellipse shape.
	'''
	Figure8Parallel = 1,
	'''
	The pattern uses a figure 8 shape that is parallel to the vector path.
	'''
	Figure8Perpendicular = 2,
	'''
	The pattern uses a figure 8 shape that is perpendicular to the vector path.
	'''

class PsoDistanceCounterResetMask(CEnum):
	'''
	Specifies the conditions that will reset the PSO distance counters.
	'''
	_init_ = 'value __doc__',
	ResetUntilMarker = 1,
	'''
	The counters will be held in reset until the first marker is encountered.
	'''
	ResetOnMarker = 2,
	'''
	The counters will reset when the marker is encountered.
	'''
	ResetOutsideWindow = 4,
	'''
	The counters will be held in reset when the PSO window output is off.
	'''
	ResetWhenLaserOff = 8,
	'''
	The counters will be held in reset when the laser command bit is off.
	'''
	ResetWhenOutputOff = 16,
	'''
	The counters will be held in reset when the PSO output is off.
	'''

class PsoDistanceAllowedEventDirection(CEnum):
	'''
	Specifies the motion directions that can generate PSO events.
	'''
	_init_ = 'value __doc__',
	Both = 0,
	'''
	PSO events will be generated when the distance counter reaches the configured distance in both directions.
	'''
	Positive = 1,
	'''
	PSO events will only be generated when the distance counter reaches the configured distance in the positive direction.
	'''
	Negative = 2,
	'''
	PSO events will only be generated when the distance counter reaches the configured distance in the negative direction.
	'''

class PsoWindowUpdateDirection(CEnum):
	'''
	Specifies the directions in which exiting the active PSO window will result in the window updating to the next pair of ranges.
	'''
	_init_ = 'value __doc__',
	Both = 0,
	'''
	The PSO window range will update when exiting the active window in either direction.
	'''
	Positive = 1,
	'''
	The PSO window range will only update when exiting the active window in the positive direction.
	'''
	Negative = 2,
	'''
	The PSO window range will only update when exiting the active window in the negative direction.
	'''

class PsoWindowCounterResetMask(CEnum):
	'''
	Specifies the conditions that will reset the PSO window counters.
	'''
	_init_ = 'value __doc__',
	ResetUntilMarker = 1,
	'''
	The counters will be held in reset until the first marker is encountered.
	'''
	ResetOnMarker = 2,
	'''
	The counters will reset when the marker is encountered.
	'''

class PsoWindowEventMode(CEnum):
	'''
	Specifies the conditions that will generate a PSO event when entering or exiting the PSO window.
	'''
	_init_ = 'value __doc__',
	None_ = 0,
	'''
	An event will not be generated when entering or exiting the window.
	'''
	Enter = 1,
	'''
	An event will be generated when entering the window.
	'''
	Exit = 2,
	'''
	An event will be generated when exiting the window.
	'''
	Both = 3,
	'''
	An event will be generated when entering or exiting the window.
	'''

class PsoEventMask(CEnum):
	'''
	Specifies additional conditions to prevent PSO events from occurring.
	'''
	_init_ = 'value __doc__',
	WindowMask = 1,
	'''
	PSO events will not occur when the window output is off.
	'''
	WindowMaskInvert = 2,
	'''
	PSO events will not occur when the window output is on.
	'''
	LaserMask = 4,
	'''
	PSO events will not occur when the laser command bit is off.
	'''
	BitMask = 8,
	'''
	PSO events will not occur when the active PSO bit is 0.
	'''

class PsoWaveformMode(CEnum):
	'''
	Selects the output mode of the PSO waveform module.
	'''
	_init_ = 'value __doc__',
	Pulse = 0,
	'''
	Selects a configurable set of pulses as the PSO waveform output.
	'''
	Pwm = 1,
	'''
	Selects a configurable PWM output as the PSO waveform output.
	'''
	Toggle = 2,
	'''
	Selects a toggling output as the PSO waveform output.
	'''

class PsoWaveformPulseMask(CEnum):
	'''
	Specifies additional conditions to disable the PSO waveform output in pulse mode.
	'''
	_init_ = 'value __doc__',
	WindowMask = 1,
	'''
	PSO waveform output will be deactivated when the window output is off.
	'''
	WindowMaskInvert = 2,
	'''
	PSO waveform output will be deactivated when the window output is on.
	'''
	LaserMask = 4,
	'''
	PSO waveform output will be deactivated when the laser command bit is off.
	'''

class PsoWaveformScalingMode(CEnum):
	'''
	Specifies the scaling mode of the PSO waveform module.
	'''
	_init_ = 'value __doc__',
	ScaleTotalTimeAndOnTime = 0,
	'''
	Applies waveform scaling to the total time and on time parameters.
	'''
	ScaleOnTimeOnly = 1,
	'''
	Applies waveform scaling to the on time parameter only.
	'''
	ScaleTotalTimeOnly = 2,
	'''
	Applies waveform scaling to the total time parameter only.
	'''

class PsoWaveformScalingInput(CEnum):
	'''
	Specifies the scaling input signal of the PSO waveform module.
	'''
	_init_ = 'value __doc__',
	DrivePulseStreamVelocity = 0,
	'''
	Uses the velocity from the drive pulse stream to determine the waveform scaling value.
	'''
	AnalogInput0 = 1,
	'''
	Uses analog input 0 to determine the waveform scaling value.
	'''
	AnalogInput1 = 2,
	'''
	Uses analog input 1 to determine the waveform scaling value.
	'''
	AnalogInput2 = 3,
	'''
	Uses analog input 2 to determine the waveform scaling value.
	'''
	AnalogInput3 = 4,
	'''
	Uses analog input 3 to determine the waveform scaling value.
	'''

class PsoOutputSource(CEnum):
	'''
	Selects the internal PSO signal to drive onto the active PSO output pin.
	'''
	_init_ = 'value __doc__',
	Waveform = 1,
	'''
	The PSO output will be active when the PSO waveform output is active.
	'''
	WindowOutput = 2,
	'''
	The PSO output will be active when the PSO window output is active.
	'''
	WindowOutputInvert = 3,
	'''
	The PSO output will be active when the PSO window output is not active.
	'''
	Bitmap = 4,
	'''
	The PSO output will be active when the active PSO bit is 1.
	'''
	DataCollectionSyncPulse = 5,
	'''
	The PSO output will have a rising edge when a data collection sample is taken.
	'''
	LaserOutput = 6,
	'''
	The PSO output will be active when the laser bit is 1.
	'''

class SafeZoneType(CEnum):
	'''
	Represents a type of safe zone.
	'''
	_init_ = 'value __doc__',
	NoEnter = 0,
	'''
	Positions will stay outside of the zone.
	'''
	NoExit = 1,
	'''
	Positions will stay inside the zone.
	'''
	NoEnterAxisFault = 2,
	'''
	Positions will stay outside of the zone and a safe zone axis fault is generated if the safe zone is violated.
	'''
	NoExitAxisFault = 3,
	'''
	Positions will stay inside the zone and a safe zone axis fault is generated if the safe zone is violated.
	'''

class JoystickInput(CEnum):
	'''
	Represents a joystick input.
	'''
	_init_ = 'value __doc__',
	Input0 = 0,
	'''
	The first joystick input.
	'''
	Input1 = 1,
	'''
	The second joystick input.
	'''
	Input2 = 2,
	'''
	The third joystick input.
	'''

class GearingSource(CEnum):
	'''
	Specifies the input data source for gearing motion.
	'''
	_init_ = 'value __doc__',
	PositionFeedback = 0,
	'''
	Use Position Feedback on the leader axis as the source for gearing.
	'''
	PositionCommand = 1,
	'''
	Use Position Command on the leader axis as the source for gearing.
	'''
	AuxiliaryFeedback = 2,
	'''
	Use Auxiliary Feedback on the leader axis as the source for gearing.
	'''
	SyncPortA = 3,
	'''
	Use Sync Port A as the source for gearing.
	'''
	SyncPortB = 4,
	'''
	Use Sync Port B as the source for gearing.
	'''

class GearingFilter(CEnum):
	'''
	Gearing filter configuration option.
	'''
	_init_ = 'value __doc__',
	None_ = 1,
	'''
	No filter is applied to the gearing motion.
	'''
	Filtered = 2,
	'''
	Low-pass filter is applied to the gearing motion.
	'''

class CammingUnits(CEnum):
	'''
	Units for the camming table values.
	'''
	_init_ = 'value __doc__',
	Primary = 0,
	'''
	Primary units.
	'''
	Secondary = 1,
	'''
	Secondary units.
	'''
	Counts = 2,
	'''
	Values in counts.
	'''

class CammingInterpolation(CEnum):
	'''
	Interpolation mode for camming.
	'''
	_init_ = 'value __doc__',
	Linear = 0,
	'''
	Linear interpolation.
	'''
	Cubic = 1,
	'''
	Cubic interpolation.
	'''

class CammingWrapping(CEnum):
	'''
	Wrapping mode for the camming table.
	'''
	_init_ = 'value __doc__',
	NoWrap = 0,
	'''
	Table leader axis values will not wrap. This is the default controller behavior and is correct for most applications.
	'''
	Wrap = 1,
	'''
	Table leader axis values wrap creating a cyclic array. This is useful for rotary applications where the first position is 0 degrees and the final position is 360 degrees.
	'''

class CammingSource(CEnum):
	'''
	Specifies the input data source for camming motion.
	'''
	_init_ = 'value __doc__',
	PositionFeedback = 0,
	'''
	Use Position Feedback on the leader axis as the source for camming.
	'''
	PositionCommand = 1,
	'''
	Use Position Command on the leader axis as the source for camming.
	'''
	AuxiliaryFeedback = 2,
	'''
	Use Auxiliary Feedback on the leader axis as the source for camming.
	'''
	SyncPortA = 3,
	'''
	Use Sync Port A as the source for camming.
	'''
	SyncPortB = 4,
	'''
	Use Sync Port B as the source for camming.
	'''

class CammingOutput(CEnum):
	'''
	Specifies the output signal to generate on the camming follower axis. Also specifies the leader axis and follower axis synchronization to use when camming is enabled.
	'''
	_init_ = 'value __doc__',
	RelativePosition = 1,
	'''
	The follower axis will operate in position-based relative synchronization mode. All camming table values for the follower axis are treated as absolute positions, but the follower axis will remain at the current position when camming is enabled. An offset will be applied to all follower axis positions in the camming table, and the offset is computed based on the current leader axis position and current follower axis position.
	'''
	AbsolutePosition = 2,
	'''
	The follower axis will operate in position-based absolute synchronization mode. All camming table values for the follower axis are treated as absolute positions, and the controller will perform an alignment move on the follower axis when camming is enabled. The controller moves the follower axis to the position specified in the camming table based on the current leader axis position.
	'''
	Velocity = 3,
	'''
	The follower axis will operate in velocity mode. All camming table values for the follower axis are treated as velocities, but the follower axis will remain at the current velocity when camming is enabled. An offset will be applied to all follower axis velocities in the camming table, and the offset is computed based on the current leader axis position and current follower axis velocity.
	'''

class ServoLoopGain(CEnum):
	'''
	Type of servo loop gain.
	'''
	_init_ = 'value __doc__',
	GainK = 0,
	'''
	Overall servo.
	'''
	GainKiv = 1,
	'''
	Velocity loop integral.
	'''
	GainKip = 2,
	'''
	Position loop integral.
	'''
	GainKv = 3,
	'''
	Position scaling.
	'''
	GainKpv = 4,
	'''
	Velocity loop proportional.
	'''
	GainKip2 = 5,
	'''
	Position loop pure integral.
	'''
	GainKsi1 = 6,
	'''
	Parallel integral.
	'''
	GainKsi2 = 7,
	'''
	Parallel integral.
	'''
	GainAlpha = 8,
	'''
	Dual loop scaling.
	'''

class FeedforwardGain(CEnum):
	'''
	Type of feedforward gain.
	'''
	_init_ = 'value __doc__',
	GainAff = 0,
	'''
	Acceleration.
	'''
	GainVff = 1,
	'''
	Velocity.
	'''
	GainJff = 2,
	'''
	Jerk.
	'''
	GainPff = 3,
	'''
	Position.
	'''
	GainSff = 4,
	'''
	Snap.
	'''

class EncoderOutputChannel(CEnum):
	'''
	The source used as the output channel for encoder echoing.
	'''
	_init_ = 'value __doc__',
	AuxiliaryEncoder = 0,
	'''
	Auxiliary channel.
	'''
	SyncPortA = 1,
	'''
	Sync Port A channel.
	'''
	SyncPortB = 2,
	'''
	Sync Port B channel.
	'''
	HighSpeedOutputs = 3,
	'''
	High Speed Output channel.
	'''
	EncoderOutputConnector = 4,
	'''
	Encoder Output Connector channel.
	'''

class EncoderInputChannel(CEnum):
	'''
	The source used as the input channel for encoder echoing.
	'''
	_init_ = 'value __doc__',
	PrimaryEncoder = 0,
	'''
	Primary channel.
	'''
	AuxiliaryEncoder = 1,
	'''
	Auxiliary channel.
	'''
	SyncPortA = 2,
	'''
	Sync Port A channel.
	'''
	SyncPortB = 3,
	'''
	Sync Port B channel.
	'''
	PulseStream = 4,
	'''
	Pulse Stream channel.
	'''

class EncoderOutputMode(CEnum):
	'''
	The mode used for encoder echoing.
	'''
	_init_ = 'value __doc__',
	Default = 0,
	'''
	The controller will use the DriveEncoderOutputConfigureInput() configuration to determine if the output signal is Quadrature or Clock and Direction.
	'''
	Quadrature = 0,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to Default. Use Default instead of this enum value.
	'''

class DrivePulseStreamSignalMode(CEnum):
	'''
	The signal mode used when DriveEncoderOutputConfigureInput() and DriveEncoderOutputOn() are configured to echo the Pulse Stream signal to an encoder output.
	'''
	_init_ = 'value __doc__',
	Quadrature = 0,
	'''
	Quadrature mode.
	'''
	ClockDirection = 1,
	'''
	Clock and Direction mode.
	'''

class AnalogOutputUpdateEvent(CEnum):
	'''
	Specifies the event which causes a new analog output value to be read from the drive array and sent to the output.
	'''
	_init_ = 'value __doc__',
	Time = 0,
	'''
	Updates will occur at a specific rate.
	'''
	PsoEvent = 1,
	'''
	Updates will occur on a PSO event.
	'''
	PsoOutput = 2,
	'''
	Updates will occur on the rising edge of PSO output.
	'''

class DriveDataCaptureInput(CEnum):
	'''
	Specifies the item that will be stored when the Drive Data Capture trigger occurs.
	'''
	_init_ = 'value __doc__',
	PositionCommand = 0,
	'''
	Position Command.
	'''
	PrimaryFeedback = 1,
	'''
	Primary Feedback.
	'''
	AuxiliaryFeedback = 2,
	'''
	Auxiliary Feedback.
	'''
	AnalogInput0 = 3,
	'''
	Analog Input 0.
	'''
	AnalogInput1 = 4,
	'''
	Analog Input 1.
	'''
	AnalogInput2 = 5,
	'''
	Analog Input 2.
	'''
	AnalogInput3 = 6,
	'''
	Analog Input 3.
	'''
	PositionFeedback = 7,
	'''
	Position Feedback.
	'''
	SyncPortA = 8,
	'''
	Sync Port A.
	'''
	SyncPortB = 9,
	'''
	Sync Port B.
	'''
	PsoCounter0 = 10,
	'''
	PSO Counter 0.
	'''
	PsoCounter1 = 11,
	'''
	PSO Counter 1.
	'''
	PsoCounter2 = 12,
	'''
	PSO Counter 2.
	'''
	PsoWindow0 = 13,
	'''
	PSO Window 0.
	'''
	PsoWindow1 = 14,
	'''
	PSO Window 1.
	'''

class DriveDataCaptureTrigger(CEnum):
	'''
	Specifies the event that Drive Data Capture uses to trigger a capture of the configured source signal.
	'''
	_init_ = 'value __doc__',
	PsoOutput = 0,
	'''
	PSO output rising edge.
	'''
	PsoEvent = 1,
	'''
	PSO event.
	'''
	HighSpeedInput0RisingEdge = 2,
	'''
	High Speed Input 0 rising edge.
	'''
	HighSpeedInput0FallingEdge = 3,
	'''
	High Speed Input 0 falling edge.
	'''
	HighSpeedInput1RisingEdge = 4,
	'''
	High Speed Input 1 rising edge.
	'''
	HighSpeedInput1FallingEdge = 5,
	'''
	High Speed Input 1 falling edge.
	'''
	AuxiliaryMarkerRisingEdge = 6,
	'''
	Auxiliary Marker rising edge.
	'''
	AuxiliaryMarkerFallingEdge = 7,
	'''
	Auxiliary Marker falling edge.
	'''

class DriveArrayType(CEnum):
	'''
	Specifies the type of drive array feature to use.
	'''
	_init_ = 'value __doc__',
	AnalogOutputVoltages = 6,
	'''
	32-bit floating-point voltages.
	'''
	DataCapturePositions = 7,
	'''
	64-bit floating-point counts.
	'''
	PsoBitmapBits = 8,
	'''
	32-bit unsigned integer bitmaps.
	'''
	PsoDistanceEventDistances = 9,
	'''
	32-bit unsigned integer counts.
	'''
	PsoPulseTimes = 10,
	'''
	32-bit floating-point microseconds.
	'''
	PsoPulseCounts = 11,
	'''
	32-bit unsigned integers.
	'''
	PsoWindowRanges = 12,
	'''
	32-bit signed integer counts.
	'''

class PsoDistanceInput(CEnum):
	'''
	Specifies the PSO distance input settings for each drive.
	'''
	_init_ = 'value __doc__',
	GL4PrimaryFeedbackAxis1Encoder0 = 100,
	'''
	GL4 Primary Feedback Axis 1 Encoder 0.
	'''
	GL4PrimaryFeedbackAxis2Encoder0 = 101,
	'''
	GL4 Primary Feedback Axis 2 Encoder 0.
	'''
	GL4IfovFeedbackAxis1 = 102,
	'''
	GL4 Primary Feedback Axis 1 with IFOV input.
	'''
	GL4IfovFeedbackAxis2 = 103,
	'''
	GL4 Primary Feedback Axis 2 with IFOV input.
	'''
	GL4AuxiliaryFeedbackAxis1 = 104,
	'''
	GL4 Auxiliary Feedback Axis 1.
	'''
	GL4AuxiliaryFeedbackAxis2 = 105,
	'''
	GL4 Auxiliary Feedback Axis 2.
	'''
	GL4SyncPortA = 106,
	'''
	GL4 Sync Port A.
	'''
	GL4SyncPortB = 107,
	'''
	GL4 Sync Port B.
	'''
	GL4DrivePulseStreamAxis1 = 108,
	'''
	GL4 Drive Pulse Stream Axis 1.
	'''
	GL4DrivePulseStreamAxis2 = 109,
	'''
	GL4 Drive Pulse Stream Axis 2.
	'''
	XL4sPrimaryFeedback = 110,
	'''
	XL4s Primary Feedback.
	'''
	XL4sAuxiliaryFeedback = 111,
	'''
	XL4s Auxiliary Feedback.
	'''
	XL4sSyncPortA = 112,
	'''
	XL4s Sync Port A.
	'''
	XL4sSyncPortB = 113,
	'''
	XL4s Sync Port B.
	'''
	XL4sDrivePulseStream = 114,
	'''
	XL4s Drive Pulse Stream.
	'''
	XR3PrimaryFeedbackAxis1 = 115,
	'''
	XR3 Primary Feedback Axis 1.
	'''
	XR3PrimaryFeedbackAxis2 = 116,
	'''
	XR3 Primary Feedback Axis 2.
	'''
	XR3PrimaryFeedbackAxis3 = 117,
	'''
	XR3 Primary Feedback Axis 3.
	'''
	XR3PrimaryFeedbackAxis4 = 118,
	'''
	XR3 Primary Feedback Axis 4.
	'''
	XR3PrimaryFeedbackAxis5 = 119,
	'''
	XR3 Primary Feedback Axis 5.
	'''
	XR3PrimaryFeedbackAxis6 = 120,
	'''
	XR3 Primary Feedback Axis 6.
	'''
	XR3AuxiliaryFeedbackAxis1 = 121,
	'''
	XR3 Auxiliary Feedback Axis 1.
	'''
	XR3AuxiliaryFeedbackAxis2 = 122,
	'''
	XR3 Auxiliary Feedback Axis 2.
	'''
	XR3AuxiliaryFeedbackAxis3 = 123,
	'''
	XR3 Auxiliary Feedback Axis 3.
	'''
	XR3AuxiliaryFeedbackAxis4 = 124,
	'''
	XR3 Auxiliary Feedback Axis 4.
	'''
	XR3AuxiliaryFeedbackAxis5 = 125,
	'''
	XR3 Auxiliary Feedback Axis 5.
	'''
	XR3AuxiliaryFeedbackAxis6 = 126,
	'''
	XR3 Auxiliary Feedback Axis 6.
	'''
	XR3SyncPortA = 127,
	'''
	XR3 Sync Port A.
	'''
	XR3SyncPortB = 128,
	'''
	XR3 Sync Port B.
	'''
	XR3DrivePulseStream = 129,
	'''
	XR3 Drive Pulse Stream.
	'''
	XC4PrimaryFeedback = 130,
	'''
	XC4 Primary Feedback.
	'''
	XC4AuxiliaryFeedback = 131,
	'''
	XC4 Auxiliary Feedback.
	'''
	XC4SyncPortA = 132,
	'''
	XC4 Sync Port A.
	'''
	XC4SyncPortB = 133,
	'''
	XC4 Sync Port B.
	'''
	XC4DrivePulseStream = 134,
	'''
	XC4 Drive Pulse Stream.
	'''
	XC4ePrimaryFeedback = 135,
	'''
	XC4e Primary Feedback.
	'''
	XC4eAuxiliaryFeedback = 136,
	'''
	XC4e Auxiliary Feedback.
	'''
	XC4eSyncPortA = 137,
	'''
	XC4e Sync Port A.
	'''
	XC4eSyncPortB = 138,
	'''
	XC4e Sync Port B.
	'''
	XC4eDrivePulseStream = 139,
	'''
	XC4e Drive Pulse Stream.
	'''
	XC6ePrimaryFeedback = 140,
	'''
	XC6e Primary Feedback.
	'''
	XC6eAuxiliaryFeedback = 141,
	'''
	XC6e Auxiliary Feedback.
	'''
	XC6eSyncPortA = 142,
	'''
	XC6e Sync Port A.
	'''
	XC6eSyncPortB = 143,
	'''
	XC6e Sync Port B.
	'''
	XC6eDrivePulseStream = 144,
	'''
	XC6e Drive Pulse Stream.
	'''
	XL5ePrimaryFeedback = 145,
	'''
	XL5e Primary Feedback.
	'''
	XL5eAuxiliaryFeedback = 146,
	'''
	XL5e Auxiliary Feedback.
	'''
	XL5eSyncPortA = 147,
	'''
	XL5e Sync Port A.
	'''
	XL5eSyncPortB = 148,
	'''
	XL5e Sync Port B.
	'''
	XL5eDrivePulseStream = 149,
	'''
	XL5e Drive Pulse Stream.
	'''
	XC2PrimaryFeedback = 150,
	'''
	XC2 Primary Feedback.
	'''
	XC2AuxiliaryFeedback = 151,
	'''
	XC2 Auxiliary Feedback.
	'''
	XC2DrivePulseStream = 152,
	'''
	XC2 Drive Pulse Stream.
	'''
	XC2ePrimaryFeedback = 153,
	'''
	XC2e Primary Feedback.
	'''
	XC2eAuxiliaryFeedback = 154,
	'''
	XC2e Auxiliary Feedback.
	'''
	XC2eDrivePulseStream = 155,
	'''
	XC2e Drive Pulse Stream.
	'''
	XL2ePrimaryFeedback = 156,
	'''
	XL2e Primary Feedback.
	'''
	XL2eAuxiliaryFeedback = 157,
	'''
	XL2e Auxiliary Feedback.
	'''
	XL2eSyncPortA = 158,
	'''
	XL2e Sync Port A.
	'''
	XL2eSyncPortB = 159,
	'''
	XL2e Sync Port B.
	'''
	XL2eDrivePulseStream = 160,
	'''
	XL2e Drive Pulse Stream.
	'''
	XI4PrimaryFeedbackAxis1 = 161,
	'''
	XI4 Primary Feedback Axis 1.
	'''
	XI4PrimaryFeedbackAxis2 = 162,
	'''
	XI4 Primary Feedback Axis 2.
	'''
	XI4PrimaryFeedbackAxis3 = 163,
	'''
	XI4 Primary Feedback Axis 3.
	'''
	XI4PrimaryFeedbackAxis4 = 164,
	'''
	XI4 Primary Feedback Axis 4.
	'''
	XI4AuxiliaryFeedbackAxis1 = 165,
	'''
	XI4 Auxiliary Feedback Axis 1.
	'''
	XI4AuxiliaryFeedbackAxis2 = 166,
	'''
	XI4 Auxiliary Feedback Axis 2.
	'''
	XI4AuxiliaryFeedbackAxis3 = 167,
	'''
	XI4 Auxiliary Feedback Axis 3.
	'''
	XI4AuxiliaryFeedbackAxis4 = 168,
	'''
	XI4 Auxiliary Feedback Axis 4.
	'''
	XI4SyncPortA = 169,
	'''
	XI4 Sync Port A.
	'''
	XI4SyncPortB = 170,
	'''
	XI4 Sync Port B.
	'''
	XI4DrivePulseStreamAxis1 = 171,
	'''
	XI4 Drive Pulse Stream Axis 1.
	'''
	XI4DrivePulseStreamAxis2 = 172,
	'''
	XI4 Drive Pulse Stream Axis 2.
	'''
	XI4DrivePulseStreamAxis3 = 173,
	'''
	XI4 Drive Pulse Stream Axis 3.
	'''
	XI4DrivePulseStreamAxis4 = 174,
	'''
	XI4 Drive Pulse Stream Axis 4.
	'''
	iXC4PrimaryFeedback = 175,
	'''
	iXC4 Primary Feedback.
	'''
	iXC4AuxiliaryFeedback = 176,
	'''
	iXC4 Auxiliary Feedback.
	'''
	iXC4SyncPortA = 177,
	'''
	iXC4 Sync Port A.
	'''
	iXC4SyncPortB = 178,
	'''
	iXC4 Sync Port B.
	'''
	iXC4DrivePulseStream = 179,
	'''
	iXC4 Drive Pulse Stream.
	'''
	iXC4ePrimaryFeedback = 180,
	'''
	iXC4e Primary Feedback.
	'''
	iXC4eAuxiliaryFeedback = 181,
	'''
	iXC4e Auxiliary Feedback.
	'''
	iXC4eSyncPortA = 182,
	'''
	iXC4e Sync Port A.
	'''
	iXC4eSyncPortB = 183,
	'''
	iXC4e Sync Port B.
	'''
	iXC4eDrivePulseStream = 184,
	'''
	iXC4e Drive Pulse Stream.
	'''
	iXC6ePrimaryFeedback = 185,
	'''
	iXC6e Primary Feedback.
	'''
	iXC6eAuxiliaryFeedback = 186,
	'''
	iXC6e Auxiliary Feedback.
	'''
	iXC6eSyncPortA = 187,
	'''
	iXC6e Sync Port A.
	'''
	iXC6eSyncPortB = 188,
	'''
	iXC6e Sync Port B.
	'''
	iXC6eDrivePulseStream = 189,
	'''
	iXC6e Drive Pulse Stream.
	'''
	iXL5ePrimaryFeedback = 190,
	'''
	iXL5e Primary Feedback.
	'''
	iXL5eAuxiliaryFeedback = 191,
	'''
	iXL5e Auxiliary Feedback.
	'''
	iXL5eSyncPortA = 192,
	'''
	iXL5e Sync Port A.
	'''
	iXL5eSyncPortB = 193,
	'''
	iXL5e Sync Port B.
	'''
	iXL5eDrivePulseStream = 194,
	'''
	iXL5e Drive Pulse Stream.
	'''
	iXR3PrimaryFeedbackAxis1 = 195,
	'''
	iXR3 Primary Feedback Axis 1.
	'''
	iXR3PrimaryFeedbackAxis2 = 196,
	'''
	iXR3 Primary Feedback Axis 2.
	'''
	iXR3PrimaryFeedbackAxis3 = 197,
	'''
	iXR3 Primary Feedback Axis 3.
	'''
	iXR3PrimaryFeedbackAxis4 = 198,
	'''
	iXR3 Primary Feedback Axis 4.
	'''
	iXR3PrimaryFeedbackAxis5 = 199,
	'''
	iXR3 Primary Feedback Axis 5.
	'''
	iXR3PrimaryFeedbackAxis6 = 200,
	'''
	iXR3 Primary Feedback Axis 6.
	'''
	iXR3AuxiliaryFeedbackAxis1 = 201,
	'''
	iXR3 Auxiliary Feedback Axis 1.
	'''
	iXR3AuxiliaryFeedbackAxis2 = 202,
	'''
	iXR3 Auxiliary Feedback Axis 2.
	'''
	iXR3AuxiliaryFeedbackAxis3 = 203,
	'''
	iXR3 Auxiliary Feedback Axis 3.
	'''
	iXR3AuxiliaryFeedbackAxis4 = 204,
	'''
	iXR3 Auxiliary Feedback Axis 4.
	'''
	iXR3AuxiliaryFeedbackAxis5 = 205,
	'''
	iXR3 Auxiliary Feedback Axis 5.
	'''
	iXR3AuxiliaryFeedbackAxis6 = 206,
	'''
	iXR3 Auxiliary Feedback Axis 6.
	'''
	iXR3SyncPortA = 207,
	'''
	iXR3 Sync Port A.
	'''
	iXR3SyncPortB = 208,
	'''
	iXR3 Sync Port B.
	'''
	iXR3DrivePulseStream = 209,
	'''
	iXR3 Drive Pulse Stream.
	'''
	GI4DrivePulseStreamAxis1 = 210,
	'''
	GI4 Drive Pulse Stream Axis 1.
	'''
	GI4DrivePulseStreamAxis2 = 211,
	'''
	GI4 Drive Pulse Stream Axis 2.
	'''
	GI4DrivePulseStreamAxis3 = 212,
	'''
	GI4 Drive Pulse Stream Axis 3.
	'''
	iXC2PrimaryFeedback = 213,
	'''
	iXC2 Primary Feedback.
	'''
	iXC2AuxiliaryFeedback = 214,
	'''
	iXC2 Auxiliary Feedback.
	'''
	iXC2DrivePulseStream = 215,
	'''
	iXC2 Drive Pulse Stream.
	'''
	iXC2ePrimaryFeedback = 216,
	'''
	iXC2e Primary Feedback.
	'''
	iXC2eAuxiliaryFeedback = 217,
	'''
	iXC2e Auxiliary Feedback.
	'''
	iXC2eDrivePulseStream = 218,
	'''
	iXC2e Drive Pulse Stream.
	'''
	iXL2ePrimaryFeedback = 219,
	'''
	iXL2e Primary Feedback.
	'''
	iXL2eAuxiliaryFeedback = 220,
	'''
	iXL2e Auxiliary Feedback.
	'''
	iXL2eSyncPortA = 221,
	'''
	iXL2e Sync Port A.
	'''
	iXL2eSyncPortB = 222,
	'''
	iXL2e Sync Port B.
	'''
	iXL2eDrivePulseStream = 223,
	'''
	iXL2e Drive Pulse Stream.
	'''
	iXI4PrimaryFeedbackAxis1 = 224,
	'''
	iXI4 Primary Feedback Axis 1.
	'''
	iXI4PrimaryFeedbackAxis2 = 225,
	'''
	iXI4 Primary Feedback Axis 2.
	'''
	iXI4PrimaryFeedbackAxis3 = 226,
	'''
	iXI4 Primary Feedback Axis 3.
	'''
	iXI4PrimaryFeedbackAxis4 = 227,
	'''
	iXI4 Primary Feedback Axis 4.
	'''
	iXI4AuxiliaryFeedbackAxis1 = 228,
	'''
	iXI4 Auxiliary Feedback Axis 1.
	'''
	iXI4AuxiliaryFeedbackAxis2 = 229,
	'''
	iXI4 Auxiliary Feedback Axis 2.
	'''
	iXI4AuxiliaryFeedbackAxis3 = 230,
	'''
	iXI4 Auxiliary Feedback Axis 3.
	'''
	iXI4AuxiliaryFeedbackAxis4 = 231,
	'''
	iXI4 Auxiliary Feedback Axis 4.
	'''
	iXI4SyncPortA = 232,
	'''
	iXI4 Sync Port A.
	'''
	iXI4SyncPortB = 233,
	'''
	iXI4 Sync Port B.
	'''
	iXI4DrivePulseStreamAxis1 = 234,
	'''
	iXI4 Drive Pulse Stream Axis 1.
	'''
	iXI4DrivePulseStreamAxis2 = 235,
	'''
	iXI4 Drive Pulse Stream Axis 2.
	'''
	iXI4DrivePulseStreamAxis3 = 236,
	'''
	iXI4 Drive Pulse Stream Axis 3.
	'''
	iXI4DrivePulseStreamAxis4 = 237,
	'''
	iXI4 Drive Pulse Stream Axis 4.
	'''
	FLEXPrimaryFeedbackAxis1 = 238,
	'''
	FLEX Primary Feedback Axis 1.
	'''
	FLEXPrimaryFeedbackAxis2 = 239,
	'''
	FLEX Primary Feedback Axis 2.
	'''
	FLEXPrimaryFeedbackAxis3 = 240,
	'''
	FLEX Primary Feedback Axis 3.
	'''
	FLEXPrimaryFeedbackAxis4 = 241,
	'''
	FLEX Primary Feedback Axis 4.
	'''
	FLEXAuxiliaryFeedbackAxis1 = 242,
	'''
	FLEX Auxiliary Feedback Axis 1.
	'''
	FLEXAuxiliaryFeedbackAxis2 = 243,
	'''
	FLEX Auxiliary Feedback Axis 2.
	'''
	FLEXAuxiliaryFeedbackAxis3 = 244,
	'''
	FLEX Auxiliary Feedback Axis 3.
	'''
	FLEXAuxiliaryFeedbackAxis4 = 245,
	'''
	FLEX Auxiliary Feedback Axis 4.
	'''
	FLEXSyncPortA = 246,
	'''
	FLEX Sync Port A.
	'''
	FLEXSyncPortB = 247,
	'''
	FLEX Sync Port B.
	'''
	FLEXDrivePulseStreamAxis1 = 248,
	'''
	FLEX Drive Pulse Stream Axis 1.
	'''
	FLEXDrivePulseStreamAxis2 = 249,
	'''
	FLEX Drive Pulse Stream Axis 2.
	'''
	FLEXDrivePulseStreamAxis3 = 250,
	'''
	FLEX Drive Pulse Stream Axis 3.
	'''
	FLEXDrivePulseStreamAxis4 = 251,
	'''
	FLEX Drive Pulse Stream Axis 4.
	'''
	iFLEXPrimaryFeedbackAxis1 = 252,
	'''
	iFLEX Primary Feedback Axis 1.
	'''
	iFLEXPrimaryFeedbackAxis2 = 253,
	'''
	iFLEX Primary Feedback Axis 2.
	'''
	iFLEXPrimaryFeedbackAxis3 = 254,
	'''
	iFLEX Primary Feedback Axis 3.
	'''
	iFLEXPrimaryFeedbackAxis4 = 255,
	'''
	iFLEX Primary Feedback Axis 4.
	'''
	iFLEXAuxiliaryFeedbackAxis1 = 256,
	'''
	iFLEX Auxiliary Feedback Axis 1.
	'''
	iFLEXAuxiliaryFeedbackAxis2 = 257,
	'''
	iFLEX Auxiliary Feedback Axis 2.
	'''
	iFLEXAuxiliaryFeedbackAxis3 = 258,
	'''
	iFLEX Auxiliary Feedback Axis 3.
	'''
	iFLEXAuxiliaryFeedbackAxis4 = 259,
	'''
	iFLEX Auxiliary Feedback Axis 4.
	'''
	iFLEXSyncPortA = 260,
	'''
	iFLEX Sync Port A.
	'''
	iFLEXSyncPortB = 261,
	'''
	iFLEX Sync Port B.
	'''
	iFLEXDrivePulseStreamAxis1 = 262,
	'''
	iFLEX Drive Pulse Stream Axis 1.
	'''
	iFLEXDrivePulseStreamAxis2 = 263,
	'''
	iFLEX Drive Pulse Stream Axis 2.
	'''
	iFLEXDrivePulseStreamAxis3 = 264,
	'''
	iFLEX Drive Pulse Stream Axis 3.
	'''
	iFLEXDrivePulseStreamAxis4 = 265,
	'''
	iFLEX Drive Pulse Stream Axis 4.
	'''
	XA4PrimaryFeedbackAxis1 = 266,
	'''
	XA4 Primary Feedback Axis 1.
	'''
	XA4PrimaryFeedbackAxis2 = 267,
	'''
	XA4 Primary Feedback Axis 2.
	'''
	XA4DrivePulseStreamAxis1 = 268,
	'''
	XA4 Drive Pulse Stream Axis 1.
	'''
	XA4DrivePulseStreamAxis2 = 269,
	'''
	XA4 Drive Pulse Stream Axis 2.
	'''
	iXA4PrimaryFeedbackAxis1 = 270,
	'''
	iXA4 Primary Feedback Axis 1.
	'''
	iXA4PrimaryFeedbackAxis2 = 271,
	'''
	iXA4 Primary Feedback Axis 2.
	'''
	iXA4DrivePulseStreamAxis1 = 272,
	'''
	iXA4 Drive Pulse Stream Axis 1.
	'''
	iXA4DrivePulseStreamAxis2 = 273,
	'''
	iXA4 Drive Pulse Stream Axis 2.
	'''
	XA4PrimaryFeedbackAxis3 = 274,
	'''
	XA4 Primary Feedback Axis 3.
	'''
	XA4PrimaryFeedbackAxis4 = 275,
	'''
	XA4 Primary Feedback Axis 4.
	'''
	XA4DrivePulseStreamAxis3 = 276,
	'''
	XA4 Drive Pulse Stream Axis 3.
	'''
	XA4DrivePulseStreamAxis4 = 277,
	'''
	XA4 Drive Pulse Stream Axis 4.
	'''
	iXA4PrimaryFeedbackAxis3 = 278,
	'''
	iXA4 Primary Feedback Axis 3.
	'''
	iXA4PrimaryFeedbackAxis4 = 279,
	'''
	iXA4 Primary Feedback Axis 4.
	'''
	iXA4DrivePulseStreamAxis3 = 280,
	'''
	iXA4 Drive Pulse Stream Axis 3.
	'''
	iXA4DrivePulseStreamAxis4 = 281,
	'''
	iXA4 Drive Pulse Stream Axis 4.
	'''
	XA4SyncPortA = 282,
	'''
	XA4 Sync Port A.
	'''
	XA4SyncPortB = 283,
	'''
	XA4 Sync Port B.
	'''
	iXA4SyncPortA = 284,
	'''
	iXA4 Sync Port A.
	'''
	iXA4SyncPortB = 285,
	'''
	iXA4 Sync Port B.
	'''
	XA4AuxiliaryFeedback = 286,
	'''
	XA4 Auxiliary Feedback.
	'''
	iXA4AuxiliaryFeedback = 287,
	'''
	iXA4 Auxiliary Feedback.
	'''
	PsoTransformationChannel0Output = 288,
	'''
	PSO Transformation Module Channel 0 Output.
	'''
	PsoTransformationChannel1Output = 289,
	'''
	PSO Transformation Module Channel 1 Output.
	'''
	PsoTransformationChannel2Output = 290,
	'''
	PSO Transformation Module Channel 2 Output.
	'''
	PsoTransformationChannel3Output = 291,
	'''
	PSO Transformation Module Channel 3 Output.
	'''
	GL4PrimaryFeedbackAxis1Encoder1 = 292,
	'''
	GL4 Primary Feedback Axis 1 Encoder 1.
	'''
	GL4PrimaryFeedbackAxis2Encoder1 = 293,
	'''
	GL4 Primary Feedback Axis 2 Encoder 1.
	'''
	GL4PrimaryFeedbackAxis1 = 100,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to GL4PrimaryFeedbackAxis1Encoder0. Use GL4PrimaryFeedbackAxis1Encoder0 instead of this enum value.
	'''
	GL4PrimaryFeedbackAxis2 = 101,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to GL4PrimaryFeedbackAxis2Encoder0. Use GL4PrimaryFeedbackAxis2Encoder0 instead of this enum value.
	'''
	XI4AuxiliaryFeedback1 = 165,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis1. Use XI4AuxiliaryFeedbackAxis1 instead of this enum value.
	'''
	XI4AuxiliaryFeedback2 = 166,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis2. Use XI4AuxiliaryFeedbackAxis2 instead of this enum value.
	'''
	XI4AuxiliaryFeedback3 = 167,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis3. Use XI4AuxiliaryFeedbackAxis3 instead of this enum value.
	'''
	XI4AuxiliaryFeedback4 = 168,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis4. Use XI4AuxiliaryFeedbackAxis4 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback1 = 228,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis1. Use iXI4AuxiliaryFeedbackAxis1 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback2 = 229,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis2. Use iXI4AuxiliaryFeedbackAxis2 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback3 = 230,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis3. Use iXI4AuxiliaryFeedbackAxis3 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback4 = 231,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis4. Use iXI4AuxiliaryFeedbackAxis4 instead of this enum value.
	'''

class PsoWindowInput(CEnum):
	'''
	Specifies the PSO window input settings for each drive.
	'''
	_init_ = 'value __doc__',
	GL4PrimaryFeedbackAxis1Encoder0 = 100,
	'''
	GL4 Primary Feedback Axis 1 Encoder 0.
	'''
	GL4PrimaryFeedbackAxis2Encoder0 = 101,
	'''
	GL4 Primary Feedback Axis 2 Encoder 0.
	'''
	GL4IfovFeedbackAxis1 = 102,
	'''
	GL4 Primary Feedback Axis 1 with IFOV input.
	'''
	GL4IfovFeedbackAxis2 = 103,
	'''
	GL4 Primary Feedback Axis 2 with IFOV input.
	'''
	GL4AuxiliaryFeedbackAxis1 = 104,
	'''
	GL4 Auxiliary Feedback Axis 1.
	'''
	GL4AuxiliaryFeedbackAxis2 = 105,
	'''
	GL4 Auxiliary Feedback Axis 2.
	'''
	GL4SyncPortA = 106,
	'''
	GL4 Sync Port A.
	'''
	GL4SyncPortB = 107,
	'''
	GL4 Sync Port B.
	'''
	GL4DrivePulseStreamAxis1 = 108,
	'''
	GL4 Drive Pulse Stream Axis 1.
	'''
	GL4DrivePulseStreamAxis2 = 109,
	'''
	GL4 Drive Pulse Stream Axis 2.
	'''
	XL4sPrimaryFeedback = 110,
	'''
	XL4s Primary Feedback.
	'''
	XL4sAuxiliaryFeedback = 111,
	'''
	XL4s Auxiliary Feedback.
	'''
	XL4sSyncPortA = 112,
	'''
	XL4s Sync Port A.
	'''
	XL4sSyncPortB = 113,
	'''
	XL4s Sync Port B.
	'''
	XL4sDrivePulseStream = 114,
	'''
	XL4s Drive Pulse Stream.
	'''
	XR3PrimaryFeedbackAxis1 = 115,
	'''
	XR3 Primary Feedback Axis 1.
	'''
	XR3PrimaryFeedbackAxis2 = 116,
	'''
	XR3 Primary Feedback Axis 2.
	'''
	XR3PrimaryFeedbackAxis3 = 117,
	'''
	XR3 Primary Feedback Axis 3.
	'''
	XR3PrimaryFeedbackAxis4 = 118,
	'''
	XR3 Primary Feedback Axis 4.
	'''
	XR3PrimaryFeedbackAxis5 = 119,
	'''
	XR3 Primary Feedback Axis 5.
	'''
	XR3PrimaryFeedbackAxis6 = 120,
	'''
	XR3 Primary Feedback Axis 6.
	'''
	XR3AuxiliaryFeedbackAxis1 = 121,
	'''
	XR3 Auxiliary Feedback Axis 1.
	'''
	XR3AuxiliaryFeedbackAxis2 = 122,
	'''
	XR3 Auxiliary Feedback Axis 2.
	'''
	XR3AuxiliaryFeedbackAxis3 = 123,
	'''
	XR3 Auxiliary Feedback Axis 3.
	'''
	XR3AuxiliaryFeedbackAxis4 = 124,
	'''
	XR3 Auxiliary Feedback Axis 4.
	'''
	XR3AuxiliaryFeedbackAxis5 = 125,
	'''
	XR3 Auxiliary Feedback Axis 5.
	'''
	XR3AuxiliaryFeedbackAxis6 = 126,
	'''
	XR3 Auxiliary Feedback Axis 6.
	'''
	XR3SyncPortA = 127,
	'''
	XR3 Sync Port A.
	'''
	XR3SyncPortB = 128,
	'''
	XR3 Sync Port B.
	'''
	XR3DrivePulseStream = 129,
	'''
	XR3 Drive Pulse Stream.
	'''
	XC4PrimaryFeedback = 130,
	'''
	XC4 Primary Feedback.
	'''
	XC4AuxiliaryFeedback = 131,
	'''
	XC4 Auxiliary Feedback.
	'''
	XC4SyncPortA = 132,
	'''
	XC4 Sync Port A.
	'''
	XC4SyncPortB = 133,
	'''
	XC4 Sync Port B.
	'''
	XC4DrivePulseStream = 134,
	'''
	XC4 Drive Pulse Stream.
	'''
	XC4ePrimaryFeedback = 135,
	'''
	XC4e Primary Feedback.
	'''
	XC4eAuxiliaryFeedback = 136,
	'''
	XC4e Auxiliary Feedback.
	'''
	XC4eSyncPortA = 137,
	'''
	XC4e Sync Port A.
	'''
	XC4eSyncPortB = 138,
	'''
	XC4e Sync Port B.
	'''
	XC4eDrivePulseStream = 139,
	'''
	XC4e Drive Pulse Stream.
	'''
	XC6ePrimaryFeedback = 140,
	'''
	XC6e Primary Feedback.
	'''
	XC6eAuxiliaryFeedback = 141,
	'''
	XC6e Auxiliary Feedback.
	'''
	XC6eSyncPortA = 142,
	'''
	XC6e Sync Port A.
	'''
	XC6eSyncPortB = 143,
	'''
	XC6e Sync Port B.
	'''
	XC6eDrivePulseStream = 144,
	'''
	XC6e Drive Pulse Stream.
	'''
	XL5ePrimaryFeedback = 145,
	'''
	XL5e Primary Feedback.
	'''
	XL5eAuxiliaryFeedback = 146,
	'''
	XL5e Auxiliary Feedback.
	'''
	XL5eSyncPortA = 147,
	'''
	XL5e Sync Port A.
	'''
	XL5eSyncPortB = 148,
	'''
	XL5e Sync Port B.
	'''
	XL5eDrivePulseStream = 149,
	'''
	XL5e Drive Pulse Stream.
	'''
	XC2PrimaryFeedback = 150,
	'''
	XC2 Primary Feedback.
	'''
	XC2AuxiliaryFeedback = 151,
	'''
	XC2 Auxiliary Feedback.
	'''
	XC2DrivePulseStream = 152,
	'''
	XC2 Drive Pulse Stream.
	'''
	XC2ePrimaryFeedback = 153,
	'''
	XC2e Primary Feedback.
	'''
	XC2eAuxiliaryFeedback = 154,
	'''
	XC2e Auxiliary Feedback.
	'''
	XC2eDrivePulseStream = 155,
	'''
	XC2e Drive Pulse Stream.
	'''
	XL2ePrimaryFeedback = 156,
	'''
	XL2e Primary Feedback.
	'''
	XL2eAuxiliaryFeedback = 157,
	'''
	XL2e Auxiliary Feedback.
	'''
	XL2eSyncPortA = 158,
	'''
	XL2e Sync Port A.
	'''
	XL2eSyncPortB = 159,
	'''
	XL2e Sync Port B.
	'''
	XL2eDrivePulseStream = 160,
	'''
	XL2e Drive Pulse Stream.
	'''
	XI4PrimaryFeedbackAxis1 = 161,
	'''
	XI4 Primary Feedback Axis 1.
	'''
	XI4PrimaryFeedbackAxis2 = 162,
	'''
	XI4 Primary Feedback Axis 2.
	'''
	XI4PrimaryFeedbackAxis3 = 163,
	'''
	XI4 Primary Feedback Axis 3.
	'''
	XI4PrimaryFeedbackAxis4 = 164,
	'''
	XI4 Primary Feedback Axis 4.
	'''
	XI4AuxiliaryFeedbackAxis1 = 165,
	'''
	XI4 Auxiliary Feedback Axis 1.
	'''
	XI4AuxiliaryFeedbackAxis2 = 166,
	'''
	XI4 Auxiliary Feedback Axis 2.
	'''
	XI4AuxiliaryFeedbackAxis3 = 167,
	'''
	XI4 Auxiliary Feedback Axis 3.
	'''
	XI4AuxiliaryFeedbackAxis4 = 168,
	'''
	XI4 Auxiliary Feedback Axis 4.
	'''
	XI4SyncPortA = 169,
	'''
	XI4 Sync Port A.
	'''
	XI4SyncPortB = 170,
	'''
	XI4 Sync Port B.
	'''
	XI4DrivePulseStreamAxis1 = 171,
	'''
	XI4 Drive Pulse Stream Axis 1.
	'''
	XI4DrivePulseStreamAxis2 = 172,
	'''
	XI4 Drive Pulse Stream Axis 2.
	'''
	XI4DrivePulseStreamAxis3 = 173,
	'''
	XI4 Drive Pulse Stream Axis 3.
	'''
	XI4DrivePulseStreamAxis4 = 174,
	'''
	XI4 Drive Pulse Stream Axis 4.
	'''
	iXC4PrimaryFeedback = 175,
	'''
	iXC4 Primary Feedback.
	'''
	iXC4AuxiliaryFeedback = 176,
	'''
	iXC4 Auxiliary Feedback.
	'''
	iXC4SyncPortA = 177,
	'''
	iXC4 Sync Port A.
	'''
	iXC4SyncPortB = 178,
	'''
	iXC4 Sync Port B.
	'''
	iXC4DrivePulseStream = 179,
	'''
	iXC4 Drive Pulse Stream.
	'''
	iXC4ePrimaryFeedback = 180,
	'''
	iXC4e Primary Feedback.
	'''
	iXC4eAuxiliaryFeedback = 181,
	'''
	iXC4e Auxiliary Feedback.
	'''
	iXC4eSyncPortA = 182,
	'''
	iXC4e Sync Port A.
	'''
	iXC4eSyncPortB = 183,
	'''
	iXC4e Sync Port B.
	'''
	iXC4eDrivePulseStream = 184,
	'''
	iXC4e Drive Pulse Stream.
	'''
	iXC6ePrimaryFeedback = 185,
	'''
	iXC6e Primary Feedback.
	'''
	iXC6eAuxiliaryFeedback = 186,
	'''
	iXC6e Auxiliary Feedback.
	'''
	iXC6eSyncPortA = 187,
	'''
	iXC6e Sync Port A.
	'''
	iXC6eSyncPortB = 188,
	'''
	iXC6e Sync Port B.
	'''
	iXC6eDrivePulseStream = 189,
	'''
	iXC6e Drive Pulse Stream.
	'''
	iXL5ePrimaryFeedback = 190,
	'''
	iXL5e Primary Feedback.
	'''
	iXL5eAuxiliaryFeedback = 191,
	'''
	iXL5e Auxiliary Feedback.
	'''
	iXL5eSyncPortA = 192,
	'''
	iXL5e Sync Port A.
	'''
	iXL5eSyncPortB = 193,
	'''
	iXL5e Sync Port B.
	'''
	iXL5eDrivePulseStream = 194,
	'''
	iXL5e Drive Pulse Stream.
	'''
	iXR3PrimaryFeedbackAxis1 = 195,
	'''
	iXR3 Primary Feedback Axis 1.
	'''
	iXR3PrimaryFeedbackAxis2 = 196,
	'''
	iXR3 Primary Feedback Axis 2.
	'''
	iXR3PrimaryFeedbackAxis3 = 197,
	'''
	iXR3 Primary Feedback Axis 3.
	'''
	iXR3PrimaryFeedbackAxis4 = 198,
	'''
	iXR3 Primary Feedback Axis 4.
	'''
	iXR3PrimaryFeedbackAxis5 = 199,
	'''
	iXR3 Primary Feedback Axis 5.
	'''
	iXR3PrimaryFeedbackAxis6 = 200,
	'''
	iXR3 Primary Feedback Axis 6.
	'''
	iXR3AuxiliaryFeedbackAxis1 = 201,
	'''
	iXR3 Auxiliary Feedback Axis 1.
	'''
	iXR3AuxiliaryFeedbackAxis2 = 202,
	'''
	iXR3 Auxiliary Feedback Axis 2.
	'''
	iXR3AuxiliaryFeedbackAxis3 = 203,
	'''
	iXR3 Auxiliary Feedback Axis 3.
	'''
	iXR3AuxiliaryFeedbackAxis4 = 204,
	'''
	iXR3 Auxiliary Feedback Axis 4.
	'''
	iXR3AuxiliaryFeedbackAxis5 = 205,
	'''
	iXR3 Auxiliary Feedback Axis 5.
	'''
	iXR3AuxiliaryFeedbackAxis6 = 206,
	'''
	iXR3 Auxiliary Feedback Axis 6.
	'''
	iXR3SyncPortA = 207,
	'''
	iXR3 Sync Port A.
	'''
	iXR3SyncPortB = 208,
	'''
	iXR3 Sync Port B.
	'''
	iXR3DrivePulseStream = 209,
	'''
	iXR3 Drive Pulse Stream.
	'''
	GI4DrivePulseStreamAxis1 = 210,
	'''
	GI4 Drive Pulse Stream Axis 1.
	'''
	GI4DrivePulseStreamAxis2 = 211,
	'''
	GI4 Drive Pulse Stream Axis 2.
	'''
	GI4DrivePulseStreamAxis3 = 212,
	'''
	GI4 Drive Pulse Stream Axis 3.
	'''
	iXC2PrimaryFeedback = 213,
	'''
	iXC2 Primary Feedback.
	'''
	iXC2AuxiliaryFeedback = 214,
	'''
	iXC2 Auxiliary Feedback.
	'''
	iXC2DrivePulseStream = 215,
	'''
	iXC2 Drive Pulse Stream.
	'''
	iXC2ePrimaryFeedback = 216,
	'''
	iXC2e Primary Feedback.
	'''
	iXC2eAuxiliaryFeedback = 217,
	'''
	iXC2e Auxiliary Feedback.
	'''
	iXC2eDrivePulseStream = 218,
	'''
	iXC2e Drive Pulse Stream.
	'''
	iXL2ePrimaryFeedback = 219,
	'''
	iXL2e Primary Feedback.
	'''
	iXL2eAuxiliaryFeedback = 220,
	'''
	iXL2e Auxiliary Feedback.
	'''
	iXL2eSyncPortA = 221,
	'''
	iXL2e Sync Port A.
	'''
	iXL2eSyncPortB = 222,
	'''
	iXL2e Sync Port B.
	'''
	iXL2eDrivePulseStream = 223,
	'''
	iXL2e Drive Pulse Stream.
	'''
	iXI4PrimaryFeedbackAxis1 = 224,
	'''
	iXI4 Primary Feedback Axis 1.
	'''
	iXI4PrimaryFeedbackAxis2 = 225,
	'''
	iXI4 Primary Feedback Axis 2.
	'''
	iXI4PrimaryFeedbackAxis3 = 226,
	'''
	iXI4 Primary Feedback Axis 3.
	'''
	iXI4PrimaryFeedbackAxis4 = 227,
	'''
	iXI4 Primary Feedback Axis 4.
	'''
	iXI4AuxiliaryFeedbackAxis1 = 228,
	'''
	iXI4 Auxiliary Feedback Axis 1.
	'''
	iXI4AuxiliaryFeedbackAxis2 = 229,
	'''
	iXI4 Auxiliary Feedback Axis 2.
	'''
	iXI4AuxiliaryFeedbackAxis3 = 230,
	'''
	iXI4 Auxiliary Feedback Axis 3.
	'''
	iXI4AuxiliaryFeedbackAxis4 = 231,
	'''
	iXI4 Auxiliary Feedback Axis 4.
	'''
	iXI4SyncPortA = 232,
	'''
	iXI4 Sync Port A.
	'''
	iXI4SyncPortB = 233,
	'''
	iXI4 Sync Port B.
	'''
	iXI4DrivePulseStreamAxis1 = 234,
	'''
	iXI4 Drive Pulse Stream Axis 1.
	'''
	iXI4DrivePulseStreamAxis2 = 235,
	'''
	iXI4 Drive Pulse Stream Axis 2.
	'''
	iXI4DrivePulseStreamAxis3 = 236,
	'''
	iXI4 Drive Pulse Stream Axis 3.
	'''
	iXI4DrivePulseStreamAxis4 = 237,
	'''
	iXI4 Drive Pulse Stream Axis 4.
	'''
	FLEXPrimaryFeedbackAxis1 = 238,
	'''
	FLEX Primary Feedback Axis 1.
	'''
	FLEXPrimaryFeedbackAxis2 = 239,
	'''
	FLEX Primary Feedback Axis 2.
	'''
	FLEXPrimaryFeedbackAxis3 = 240,
	'''
	FLEX Primary Feedback Axis 3.
	'''
	FLEXPrimaryFeedbackAxis4 = 241,
	'''
	FLEX Primary Feedback Axis 4.
	'''
	FLEXAuxiliaryFeedbackAxis1 = 242,
	'''
	FLEX Auxiliary Feedback Axis 1.
	'''
	FLEXAuxiliaryFeedbackAxis2 = 243,
	'''
	FLEX Auxiliary Feedback Axis 2.
	'''
	FLEXAuxiliaryFeedbackAxis3 = 244,
	'''
	FLEX Auxiliary Feedback Axis 3.
	'''
	FLEXAuxiliaryFeedbackAxis4 = 245,
	'''
	FLEX Auxiliary Feedback Axis 4.
	'''
	FLEXSyncPortA = 246,
	'''
	FLEX Sync Port A.
	'''
	FLEXSyncPortB = 247,
	'''
	FLEX Sync Port B.
	'''
	FLEXDrivePulseStreamAxis1 = 248,
	'''
	FLEX Drive Pulse Stream Axis 1.
	'''
	FLEXDrivePulseStreamAxis2 = 249,
	'''
	FLEX Drive Pulse Stream Axis 2.
	'''
	FLEXDrivePulseStreamAxis3 = 250,
	'''
	FLEX Drive Pulse Stream Axis 3.
	'''
	FLEXDrivePulseStreamAxis4 = 251,
	'''
	FLEX Drive Pulse Stream Axis 4.
	'''
	iFLEXPrimaryFeedbackAxis1 = 252,
	'''
	iFLEX Primary Feedback Axis 1.
	'''
	iFLEXPrimaryFeedbackAxis2 = 253,
	'''
	iFLEX Primary Feedback Axis 2.
	'''
	iFLEXPrimaryFeedbackAxis3 = 254,
	'''
	iFLEX Primary Feedback Axis 3.
	'''
	iFLEXPrimaryFeedbackAxis4 = 255,
	'''
	iFLEX Primary Feedback Axis 4.
	'''
	iFLEXAuxiliaryFeedbackAxis1 = 256,
	'''
	iFLEX Auxiliary Feedback Axis 1.
	'''
	iFLEXAuxiliaryFeedbackAxis2 = 257,
	'''
	iFLEX Auxiliary Feedback Axis 2.
	'''
	iFLEXAuxiliaryFeedbackAxis3 = 258,
	'''
	iFLEX Auxiliary Feedback Axis 3.
	'''
	iFLEXAuxiliaryFeedbackAxis4 = 259,
	'''
	iFLEX Auxiliary Feedback Axis 4.
	'''
	iFLEXSyncPortA = 260,
	'''
	iFLEX Sync Port A.
	'''
	iFLEXSyncPortB = 261,
	'''
	iFLEX Sync Port B.
	'''
	iFLEXDrivePulseStreamAxis1 = 262,
	'''
	iFLEX Drive Pulse Stream Axis 1.
	'''
	iFLEXDrivePulseStreamAxis2 = 263,
	'''
	iFLEX Drive Pulse Stream Axis 2.
	'''
	iFLEXDrivePulseStreamAxis3 = 264,
	'''
	iFLEX Drive Pulse Stream Axis 3.
	'''
	iFLEXDrivePulseStreamAxis4 = 265,
	'''
	iFLEX Drive Pulse Stream Axis 4.
	'''
	XA4PrimaryFeedbackAxis1 = 266,
	'''
	XA4 Primary Feedback Axis 1.
	'''
	XA4PrimaryFeedbackAxis2 = 267,
	'''
	XA4 Primary Feedback Axis 2.
	'''
	XA4DrivePulseStreamAxis1 = 268,
	'''
	XA4 Drive Pulse Stream Axis 1.
	'''
	XA4DrivePulseStreamAxis2 = 269,
	'''
	XA4 Drive Pulse Stream Axis 2.
	'''
	iXA4PrimaryFeedbackAxis1 = 270,
	'''
	iXA4 Primary Feedback Axis 1.
	'''
	iXA4PrimaryFeedbackAxis2 = 271,
	'''
	iXA4 Primary Feedback Axis 2.
	'''
	iXA4DrivePulseStreamAxis1 = 272,
	'''
	iXA4 Drive Pulse Stream Axis 1.
	'''
	iXA4DrivePulseStreamAxis2 = 273,
	'''
	iXA4 Drive Pulse Stream Axis 2.
	'''
	XA4PrimaryFeedbackAxis3 = 274,
	'''
	XA4 Primary Feedback Axis 3.
	'''
	XA4PrimaryFeedbackAxis4 = 275,
	'''
	XA4 Primary Feedback Axis 4.
	'''
	XA4DrivePulseStreamAxis3 = 276,
	'''
	XA4 Drive Pulse Stream Axis 3.
	'''
	XA4DrivePulseStreamAxis4 = 277,
	'''
	XA4 Drive Pulse Stream Axis 4.
	'''
	iXA4PrimaryFeedbackAxis3 = 278,
	'''
	iXA4 Primary Feedback Axis 3.
	'''
	iXA4PrimaryFeedbackAxis4 = 279,
	'''
	iXA4 Primary Feedback Axis 4.
	'''
	iXA4DrivePulseStreamAxis3 = 280,
	'''
	iXA4 Drive Pulse Stream Axis 3.
	'''
	iXA4DrivePulseStreamAxis4 = 281,
	'''
	iXA4 Drive Pulse Stream Axis 4.
	'''
	XA4SyncPortA = 282,
	'''
	XA4 Sync Port A.
	'''
	XA4SyncPortB = 283,
	'''
	XA4 Sync Port B.
	'''
	iXA4SyncPortA = 284,
	'''
	iXA4 Sync Port A.
	'''
	iXA4SyncPortB = 285,
	'''
	iXA4 Sync Port B.
	'''
	XA4AuxiliaryFeedback = 286,
	'''
	XA4 Auxiliary Feedback.
	'''
	iXA4AuxiliaryFeedback = 287,
	'''
	iXA4 Auxiliary Feedback.
	'''
	PsoTransformationChannel0Output = 288,
	'''
	PSO Transformation Module Channel 0 Output.
	'''
	PsoTransformationChannel1Output = 289,
	'''
	PSO Transformation Module Channel 1 Output.
	'''
	PsoTransformationChannel2Output = 290,
	'''
	PSO Transformation Module Channel 2 Output.
	'''
	PsoTransformationChannel3Output = 291,
	'''
	PSO Transformation Module Channel 3 Output.
	'''
	GL4PrimaryFeedbackAxis1Encoder1 = 292,
	'''
	GL4 Primary Feedback Axis 1 Encoder 1.
	'''
	GL4PrimaryFeedbackAxis2Encoder1 = 293,
	'''
	GL4 Primary Feedback Axis 2 Encoder 1.
	'''
	GL4PrimaryFeedbackAxis1 = 100,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to GL4PrimaryFeedbackAxis1Encoder0. Use GL4PrimaryFeedbackAxis1Encoder0 instead of this enum value.
	'''
	GL4PrimaryFeedbackAxis2 = 101,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to GL4PrimaryFeedbackAxis2Encoder0. Use GL4PrimaryFeedbackAxis2Encoder0 instead of this enum value.
	'''
	XI4AuxiliaryFeedback1 = 165,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis1. Use XI4AuxiliaryFeedbackAxis1 instead of this enum value.
	'''
	XI4AuxiliaryFeedback2 = 166,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis2. Use XI4AuxiliaryFeedbackAxis2 instead of this enum value.
	'''
	XI4AuxiliaryFeedback3 = 167,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis3. Use XI4AuxiliaryFeedbackAxis3 instead of this enum value.
	'''
	XI4AuxiliaryFeedback4 = 168,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to XI4AuxiliaryFeedbackAxis4. Use XI4AuxiliaryFeedbackAxis4 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback1 = 228,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis1. Use iXI4AuxiliaryFeedbackAxis1 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback2 = 229,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis2. Use iXI4AuxiliaryFeedbackAxis2 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback3 = 230,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis3. Use iXI4AuxiliaryFeedbackAxis3 instead of this enum value.
	'''
	iXI4AuxiliaryFeedback4 = 231,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to iXI4AuxiliaryFeedbackAxis4. Use iXI4AuxiliaryFeedbackAxis4 instead of this enum value.
	'''

class PsoTransformationInput(CEnum):
	'''
	Specifies the PSO transformation input settings for each drive.
	'''
	_init_ = 'value __doc__',
	GL4PrimaryFeedbackAxis1Encoder0 = 100,
	'''
	GL4 Primary Feedback Axis 1 Encoder 0.
	'''
	GL4PrimaryFeedbackAxis2Encoder0 = 101,
	'''
	GL4 Primary Feedback Axis 2 Encoder 0.
	'''
	GL4IfovFeedbackAxis1 = 102,
	'''
	GL4 Primary Feedback Axis 1 with IFOV input.
	'''
	GL4IfovFeedbackAxis2 = 103,
	'''
	GL4 Primary Feedback Axis 2 with IFOV input.
	'''
	GL4AuxiliaryFeedbackAxis1 = 104,
	'''
	GL4 Auxiliary Feedback Axis 1.
	'''
	GL4AuxiliaryFeedbackAxis2 = 105,
	'''
	GL4 Auxiliary Feedback Axis 2.
	'''
	GL4SyncPortA = 106,
	'''
	GL4 Sync Port A.
	'''
	GL4SyncPortB = 107,
	'''
	GL4 Sync Port B.
	'''
	GL4DrivePulseStreamAxis1 = 108,
	'''
	GL4 Drive Pulse Stream Axis 1.
	'''
	GL4DrivePulseStreamAxis2 = 109,
	'''
	GL4 Drive Pulse Stream Axis 2.
	'''
	XL4sPrimaryFeedback = 110,
	'''
	XL4s Primary Feedback.
	'''
	XL4sAuxiliaryFeedback = 111,
	'''
	XL4s Auxiliary Feedback.
	'''
	XL4sSyncPortA = 112,
	'''
	XL4s Sync Port A.
	'''
	XL4sSyncPortB = 113,
	'''
	XL4s Sync Port B.
	'''
	XL4sDrivePulseStream = 114,
	'''
	XL4s Drive Pulse Stream.
	'''
	XR3PrimaryFeedbackAxis1 = 115,
	'''
	XR3 Primary Feedback Axis 1.
	'''
	XR3PrimaryFeedbackAxis2 = 116,
	'''
	XR3 Primary Feedback Axis 2.
	'''
	XR3PrimaryFeedbackAxis3 = 117,
	'''
	XR3 Primary Feedback Axis 3.
	'''
	XR3PrimaryFeedbackAxis4 = 118,
	'''
	XR3 Primary Feedback Axis 4.
	'''
	XR3PrimaryFeedbackAxis5 = 119,
	'''
	XR3 Primary Feedback Axis 5.
	'''
	XR3PrimaryFeedbackAxis6 = 120,
	'''
	XR3 Primary Feedback Axis 6.
	'''
	XR3AuxiliaryFeedbackAxis1 = 121,
	'''
	XR3 Auxiliary Feedback Axis 1.
	'''
	XR3AuxiliaryFeedbackAxis2 = 122,
	'''
	XR3 Auxiliary Feedback Axis 2.
	'''
	XR3AuxiliaryFeedbackAxis3 = 123,
	'''
	XR3 Auxiliary Feedback Axis 3.
	'''
	XR3AuxiliaryFeedbackAxis4 = 124,
	'''
	XR3 Auxiliary Feedback Axis 4.
	'''
	XR3AuxiliaryFeedbackAxis5 = 125,
	'''
	XR3 Auxiliary Feedback Axis 5.
	'''
	XR3AuxiliaryFeedbackAxis6 = 126,
	'''
	XR3 Auxiliary Feedback Axis 6.
	'''
	XR3SyncPortA = 127,
	'''
	XR3 Sync Port A.
	'''
	XR3SyncPortB = 128,
	'''
	XR3 Sync Port B.
	'''
	XR3DrivePulseStream = 129,
	'''
	XR3 Drive Pulse Stream.
	'''
	XC4PrimaryFeedback = 130,
	'''
	XC4 Primary Feedback.
	'''
	XC4AuxiliaryFeedback = 131,
	'''
	XC4 Auxiliary Feedback.
	'''
	XC4SyncPortA = 132,
	'''
	XC4 Sync Port A.
	'''
	XC4SyncPortB = 133,
	'''
	XC4 Sync Port B.
	'''
	XC4DrivePulseStream = 134,
	'''
	XC4 Drive Pulse Stream.
	'''
	XC4ePrimaryFeedback = 135,
	'''
	XC4e Primary Feedback.
	'''
	XC4eAuxiliaryFeedback = 136,
	'''
	XC4e Auxiliary Feedback.
	'''
	XC4eSyncPortA = 137,
	'''
	XC4e Sync Port A.
	'''
	XC4eSyncPortB = 138,
	'''
	XC4e Sync Port B.
	'''
	XC4eDrivePulseStream = 139,
	'''
	XC4e Drive Pulse Stream.
	'''
	XC6ePrimaryFeedback = 140,
	'''
	XC6e Primary Feedback.
	'''
	XC6eAuxiliaryFeedback = 141,
	'''
	XC6e Auxiliary Feedback.
	'''
	XC6eSyncPortA = 142,
	'''
	XC6e Sync Port A.
	'''
	XC6eSyncPortB = 143,
	'''
	XC6e Sync Port B.
	'''
	XC6eDrivePulseStream = 144,
	'''
	XC6e Drive Pulse Stream.
	'''
	XL5ePrimaryFeedback = 145,
	'''
	XL5e Primary Feedback.
	'''
	XL5eAuxiliaryFeedback = 146,
	'''
	XL5e Auxiliary Feedback.
	'''
	XL5eSyncPortA = 147,
	'''
	XL5e Sync Port A.
	'''
	XL5eSyncPortB = 148,
	'''
	XL5e Sync Port B.
	'''
	XL5eDrivePulseStream = 149,
	'''
	XL5e Drive Pulse Stream.
	'''
	XC2PrimaryFeedback = 150,
	'''
	XC2 Primary Feedback.
	'''
	XC2AuxiliaryFeedback = 151,
	'''
	XC2 Auxiliary Feedback.
	'''
	XC2DrivePulseStream = 152,
	'''
	XC2 Drive Pulse Stream.
	'''
	XC2ePrimaryFeedback = 153,
	'''
	XC2e Primary Feedback.
	'''
	XC2eAuxiliaryFeedback = 154,
	'''
	XC2e Auxiliary Feedback.
	'''
	XC2eDrivePulseStream = 155,
	'''
	XC2e Drive Pulse Stream.
	'''
	XL2ePrimaryFeedback = 156,
	'''
	XL2e Primary Feedback.
	'''
	XL2eAuxiliaryFeedback = 157,
	'''
	XL2e Auxiliary Feedback.
	'''
	XL2eSyncPortA = 158,
	'''
	XL2e Sync Port A.
	'''
	XL2eSyncPortB = 159,
	'''
	XL2e Sync Port B.
	'''
	XL2eDrivePulseStream = 160,
	'''
	XL2e Drive Pulse Stream.
	'''
	XI4PrimaryFeedbackAxis1 = 161,
	'''
	XI4 Primary Feedback Axis 1.
	'''
	XI4PrimaryFeedbackAxis2 = 162,
	'''
	XI4 Primary Feedback Axis 2.
	'''
	XI4PrimaryFeedbackAxis3 = 163,
	'''
	XI4 Primary Feedback Axis 3.
	'''
	XI4PrimaryFeedbackAxis4 = 164,
	'''
	XI4 Primary Feedback Axis 4.
	'''
	XI4AuxiliaryFeedbackAxis1 = 165,
	'''
	XI4 Auxiliary Feedback Axis 1.
	'''
	XI4AuxiliaryFeedbackAxis2 = 166,
	'''
	XI4 Auxiliary Feedback Axis 2.
	'''
	XI4AuxiliaryFeedbackAxis3 = 167,
	'''
	XI4 Auxiliary Feedback Axis 3.
	'''
	XI4AuxiliaryFeedbackAxis4 = 168,
	'''
	XI4 Auxiliary Feedback Axis 4.
	'''
	XI4SyncPortA = 169,
	'''
	XI4 Sync Port A.
	'''
	XI4SyncPortB = 170,
	'''
	XI4 Sync Port B.
	'''
	XI4DrivePulseStreamAxis1 = 171,
	'''
	XI4 Drive Pulse Stream Axis 1.
	'''
	XI4DrivePulseStreamAxis2 = 172,
	'''
	XI4 Drive Pulse Stream Axis 2.
	'''
	XI4DrivePulseStreamAxis3 = 173,
	'''
	XI4 Drive Pulse Stream Axis 3.
	'''
	XI4DrivePulseStreamAxis4 = 174,
	'''
	XI4 Drive Pulse Stream Axis 4.
	'''
	iXC4PrimaryFeedback = 175,
	'''
	iXC4 Primary Feedback.
	'''
	iXC4AuxiliaryFeedback = 176,
	'''
	iXC4 Auxiliary Feedback.
	'''
	iXC4SyncPortA = 177,
	'''
	iXC4 Sync Port A.
	'''
	iXC4SyncPortB = 178,
	'''
	iXC4 Sync Port B.
	'''
	iXC4DrivePulseStream = 179,
	'''
	iXC4 Drive Pulse Stream.
	'''
	iXC4ePrimaryFeedback = 180,
	'''
	iXC4e Primary Feedback.
	'''
	iXC4eAuxiliaryFeedback = 181,
	'''
	iXC4e Auxiliary Feedback.
	'''
	iXC4eSyncPortA = 182,
	'''
	iXC4e Sync Port A.
	'''
	iXC4eSyncPortB = 183,
	'''
	iXC4e Sync Port B.
	'''
	iXC4eDrivePulseStream = 184,
	'''
	iXC4e Drive Pulse Stream.
	'''
	iXC6ePrimaryFeedback = 185,
	'''
	iXC6e Primary Feedback.
	'''
	iXC6eAuxiliaryFeedback = 186,
	'''
	iXC6e Auxiliary Feedback.
	'''
	iXC6eSyncPortA = 187,
	'''
	iXC6e Sync Port A.
	'''
	iXC6eSyncPortB = 188,
	'''
	iXC6e Sync Port B.
	'''
	iXC6eDrivePulseStream = 189,
	'''
	iXC6e Drive Pulse Stream.
	'''
	iXL5ePrimaryFeedback = 190,
	'''
	iXL5e Primary Feedback.
	'''
	iXL5eAuxiliaryFeedback = 191,
	'''
	iXL5e Auxiliary Feedback.
	'''
	iXL5eSyncPortA = 192,
	'''
	iXL5e Sync Port A.
	'''
	iXL5eSyncPortB = 193,
	'''
	iXL5e Sync Port B.
	'''
	iXL5eDrivePulseStream = 194,
	'''
	iXL5e Drive Pulse Stream.
	'''
	iXR3PrimaryFeedbackAxis1 = 195,
	'''
	iXR3 Primary Feedback Axis 1.
	'''
	iXR3PrimaryFeedbackAxis2 = 196,
	'''
	iXR3 Primary Feedback Axis 2.
	'''
	iXR3PrimaryFeedbackAxis3 = 197,
	'''
	iXR3 Primary Feedback Axis 3.
	'''
	iXR3PrimaryFeedbackAxis4 = 198,
	'''
	iXR3 Primary Feedback Axis 4.
	'''
	iXR3PrimaryFeedbackAxis5 = 199,
	'''
	iXR3 Primary Feedback Axis 5.
	'''
	iXR3PrimaryFeedbackAxis6 = 200,
	'''
	iXR3 Primary Feedback Axis 6.
	'''
	iXR3AuxiliaryFeedbackAxis1 = 201,
	'''
	iXR3 Auxiliary Feedback Axis 1.
	'''
	iXR3AuxiliaryFeedbackAxis2 = 202,
	'''
	iXR3 Auxiliary Feedback Axis 2.
	'''
	iXR3AuxiliaryFeedbackAxis3 = 203,
	'''
	iXR3 Auxiliary Feedback Axis 3.
	'''
	iXR3AuxiliaryFeedbackAxis4 = 204,
	'''
	iXR3 Auxiliary Feedback Axis 4.
	'''
	iXR3AuxiliaryFeedbackAxis5 = 205,
	'''
	iXR3 Auxiliary Feedback Axis 5.
	'''
	iXR3AuxiliaryFeedbackAxis6 = 206,
	'''
	iXR3 Auxiliary Feedback Axis 6.
	'''
	iXR3SyncPortA = 207,
	'''
	iXR3 Sync Port A.
	'''
	iXR3SyncPortB = 208,
	'''
	iXR3 Sync Port B.
	'''
	iXR3DrivePulseStream = 209,
	'''
	iXR3 Drive Pulse Stream.
	'''
	GI4DrivePulseStreamAxis1 = 210,
	'''
	GI4 Drive Pulse Stream Axis 1.
	'''
	GI4DrivePulseStreamAxis2 = 211,
	'''
	GI4 Drive Pulse Stream Axis 2.
	'''
	GI4DrivePulseStreamAxis3 = 212,
	'''
	GI4 Drive Pulse Stream Axis 3.
	'''
	iXC2PrimaryFeedback = 213,
	'''
	iXC2 Primary Feedback.
	'''
	iXC2AuxiliaryFeedback = 214,
	'''
	iXC2 Auxiliary Feedback.
	'''
	iXC2DrivePulseStream = 215,
	'''
	iXC2 Drive Pulse Stream.
	'''
	iXC2ePrimaryFeedback = 216,
	'''
	iXC2e Primary Feedback.
	'''
	iXC2eAuxiliaryFeedback = 217,
	'''
	iXC2e Auxiliary Feedback.
	'''
	iXC2eDrivePulseStream = 218,
	'''
	iXC2e Drive Pulse Stream.
	'''
	iXL2ePrimaryFeedback = 219,
	'''
	iXL2e Primary Feedback.
	'''
	iXL2eAuxiliaryFeedback = 220,
	'''
	iXL2e Auxiliary Feedback.
	'''
	iXL2eSyncPortA = 221,
	'''
	iXL2e Sync Port A.
	'''
	iXL2eSyncPortB = 222,
	'''
	iXL2e Sync Port B.
	'''
	iXL2eDrivePulseStream = 223,
	'''
	iXL2e Drive Pulse Stream.
	'''
	iXI4PrimaryFeedbackAxis1 = 224,
	'''
	iXI4 Primary Feedback Axis 1.
	'''
	iXI4PrimaryFeedbackAxis2 = 225,
	'''
	iXI4 Primary Feedback Axis 2.
	'''
	iXI4PrimaryFeedbackAxis3 = 226,
	'''
	iXI4 Primary Feedback Axis 3.
	'''
	iXI4PrimaryFeedbackAxis4 = 227,
	'''
	iXI4 Primary Feedback Axis 4.
	'''
	iXI4AuxiliaryFeedbackAxis1 = 228,
	'''
	iXI4 Auxiliary Feedback Axis 1.
	'''
	iXI4AuxiliaryFeedbackAxis2 = 229,
	'''
	iXI4 Auxiliary Feedback Axis 2.
	'''
	iXI4AuxiliaryFeedbackAxis3 = 230,
	'''
	iXI4 Auxiliary Feedback Axis 3.
	'''
	iXI4AuxiliaryFeedbackAxis4 = 231,
	'''
	iXI4 Auxiliary Feedback Axis 4.
	'''
	iXI4SyncPortA = 232,
	'''
	iXI4 Sync Port A.
	'''
	iXI4SyncPortB = 233,
	'''
	iXI4 Sync Port B.
	'''
	iXI4DrivePulseStreamAxis1 = 234,
	'''
	iXI4 Drive Pulse Stream Axis 1.
	'''
	iXI4DrivePulseStreamAxis2 = 235,
	'''
	iXI4 Drive Pulse Stream Axis 2.
	'''
	iXI4DrivePulseStreamAxis3 = 236,
	'''
	iXI4 Drive Pulse Stream Axis 3.
	'''
	iXI4DrivePulseStreamAxis4 = 237,
	'''
	iXI4 Drive Pulse Stream Axis 4.
	'''
	FLEXPrimaryFeedbackAxis1 = 238,
	'''
	FLEX Primary Feedback Axis 1.
	'''
	FLEXPrimaryFeedbackAxis2 = 239,
	'''
	FLEX Primary Feedback Axis 2.
	'''
	FLEXPrimaryFeedbackAxis3 = 240,
	'''
	FLEX Primary Feedback Axis 3.
	'''
	FLEXPrimaryFeedbackAxis4 = 241,
	'''
	FLEX Primary Feedback Axis 4.
	'''
	FLEXAuxiliaryFeedbackAxis1 = 242,
	'''
	FLEX Auxiliary Feedback Axis 1.
	'''
	FLEXAuxiliaryFeedbackAxis2 = 243,
	'''
	FLEX Auxiliary Feedback Axis 2.
	'''
	FLEXAuxiliaryFeedbackAxis3 = 244,
	'''
	FLEX Auxiliary Feedback Axis 3.
	'''
	FLEXAuxiliaryFeedbackAxis4 = 245,
	'''
	FLEX Auxiliary Feedback Axis 4.
	'''
	FLEXSyncPortA = 246,
	'''
	FLEX Sync Port A.
	'''
	FLEXSyncPortB = 247,
	'''
	FLEX Sync Port B.
	'''
	FLEXDrivePulseStreamAxis1 = 248,
	'''
	FLEX Drive Pulse Stream Axis 1.
	'''
	FLEXDrivePulseStreamAxis2 = 249,
	'''
	FLEX Drive Pulse Stream Axis 2.
	'''
	FLEXDrivePulseStreamAxis3 = 250,
	'''
	FLEX Drive Pulse Stream Axis 3.
	'''
	FLEXDrivePulseStreamAxis4 = 251,
	'''
	FLEX Drive Pulse Stream Axis 4.
	'''
	iFLEXPrimaryFeedbackAxis1 = 252,
	'''
	iFLEX Primary Feedback Axis 1.
	'''
	iFLEXPrimaryFeedbackAxis2 = 253,
	'''
	iFLEX Primary Feedback Axis 2.
	'''
	iFLEXPrimaryFeedbackAxis3 = 254,
	'''
	iFLEX Primary Feedback Axis 3.
	'''
	iFLEXPrimaryFeedbackAxis4 = 255,
	'''
	iFLEX Primary Feedback Axis 4.
	'''
	iFLEXAuxiliaryFeedbackAxis1 = 256,
	'''
	iFLEX Auxiliary Feedback Axis 1.
	'''
	iFLEXAuxiliaryFeedbackAxis2 = 257,
	'''
	iFLEX Auxiliary Feedback Axis 2.
	'''
	iFLEXAuxiliaryFeedbackAxis3 = 258,
	'''
	iFLEX Auxiliary Feedback Axis 3.
	'''
	iFLEXAuxiliaryFeedbackAxis4 = 259,
	'''
	iFLEX Auxiliary Feedback Axis 4.
	'''
	iFLEXSyncPortA = 260,
	'''
	iFLEX Sync Port A.
	'''
	iFLEXSyncPortB = 261,
	'''
	iFLEX Sync Port B.
	'''
	iFLEXDrivePulseStreamAxis1 = 262,
	'''
	iFLEX Drive Pulse Stream Axis 1.
	'''
	iFLEXDrivePulseStreamAxis2 = 263,
	'''
	iFLEX Drive Pulse Stream Axis 2.
	'''
	iFLEXDrivePulseStreamAxis3 = 264,
	'''
	iFLEX Drive Pulse Stream Axis 3.
	'''
	iFLEXDrivePulseStreamAxis4 = 265,
	'''
	iFLEX Drive Pulse Stream Axis 4.
	'''
	XA4PrimaryFeedbackAxis1 = 266,
	'''
	XA4 Primary Feedback Axis 1.
	'''
	XA4PrimaryFeedbackAxis2 = 267,
	'''
	XA4 Primary Feedback Axis 2.
	'''
	XA4DrivePulseStreamAxis1 = 268,
	'''
	XA4 Drive Pulse Stream Axis 1.
	'''
	XA4DrivePulseStreamAxis2 = 269,
	'''
	XA4 Drive Pulse Stream Axis 2.
	'''
	iXA4PrimaryFeedbackAxis1 = 270,
	'''
	iXA4 Primary Feedback Axis 1.
	'''
	iXA4PrimaryFeedbackAxis2 = 271,
	'''
	iXA4 Primary Feedback Axis 2.
	'''
	iXA4DrivePulseStreamAxis1 = 272,
	'''
	iXA4 Drive Pulse Stream Axis 1.
	'''
	iXA4DrivePulseStreamAxis2 = 273,
	'''
	iXA4 Drive Pulse Stream Axis 2.
	'''
	XA4PrimaryFeedbackAxis3 = 274,
	'''
	XA4 Primary Feedback Axis 3.
	'''
	XA4PrimaryFeedbackAxis4 = 275,
	'''
	XA4 Primary Feedback Axis 4.
	'''
	XA4DrivePulseStreamAxis3 = 276,
	'''
	XA4 Drive Pulse Stream Axis 3.
	'''
	XA4DrivePulseStreamAxis4 = 277,
	'''
	XA4 Drive Pulse Stream Axis 4.
	'''
	iXA4PrimaryFeedbackAxis3 = 278,
	'''
	iXA4 Primary Feedback Axis 3.
	'''
	iXA4PrimaryFeedbackAxis4 = 279,
	'''
	iXA4 Primary Feedback Axis 4.
	'''
	iXA4DrivePulseStreamAxis3 = 280,
	'''
	iXA4 Drive Pulse Stream Axis 3.
	'''
	iXA4DrivePulseStreamAxis4 = 281,
	'''
	iXA4 Drive Pulse Stream Axis 4.
	'''
	XA4SyncPortA = 282,
	'''
	XA4 Sync Port A.
	'''
	XA4SyncPortB = 283,
	'''
	XA4 Sync Port B.
	'''
	iXA4SyncPortA = 284,
	'''
	iXA4 Sync Port A.
	'''
	iXA4SyncPortB = 285,
	'''
	iXA4 Sync Port B.
	'''
	XA4AuxiliaryFeedback = 286,
	'''
	XA4 Auxiliary Feedback.
	'''
	iXA4AuxiliaryFeedback = 287,
	'''
	iXA4 Auxiliary Feedback.
	'''
	PsoTransformationChannel0Output = 288,
	'''
	PSO Transformation Module Channel 0 Output.
	'''
	PsoTransformationChannel1Output = 289,
	'''
	PSO Transformation Module Channel 1 Output.
	'''
	PsoTransformationChannel2Output = 290,
	'''
	PSO Transformation Module Channel 2 Output.
	'''
	PsoTransformationChannel3Output = 291,
	'''
	PSO Transformation Module Channel 3 Output.
	'''
	GL4PrimaryFeedbackAxis1Encoder1 = 292,
	'''
	GL4 Primary Feedback Axis 1 Encoder 1.
	'''
	GL4PrimaryFeedbackAxis2Encoder1 = 293,
	'''
	GL4 Primary Feedback Axis 2 Encoder 1.
	'''

class PsoOutputPin(CEnum):
	'''
	Specifies the PSO output pin settings for each drive.
	'''
	_init_ = 'value __doc__',
	GL4None = 100,
	'''
	GL4 None (default).
	'''
	GL4LaserOutput0 = 101,
	'''
	GL4 Laser Output 0.
	'''
	XL4sNone = 102,
	'''
	XL4s None (default).
	'''
	XL4sLaserOutput0 = 103,
	'''
	XL4s Laser Output 0.
	'''
	XR3None = 104,
	'''
	XR3 None (default).
	'''
	XR3PsoOutput1 = 105,
	'''
	XR3 PSO Output 1.
	'''
	XR3PsoOutput2 = 106,
	'''
	XR3 PSO Output 2.
	'''
	XR3PsoOutput3 = 107,
	'''
	XR3 PSO Output 3.
	'''
	XC4DedicatedOutput = 108,
	'''
	XC4 Dedicated Output (default).
	'''
	XC4AuxiliaryMarkerDifferential = 109,
	'''
	XC4 Auxiliary Marker (Differential mode).
	'''
	XC4AuxiliaryMarkerSingleEnded = 110,
	'''
	XC4 Auxiliary Marker (Single-ended mode).
	'''
	XC4eDedicatedOutput = 111,
	'''
	XC4e Dedicated Output (default).
	'''
	XC4eAuxiliaryMarkerDifferential = 112,
	'''
	XC4e Auxiliary Marker (Differential mode).
	'''
	XC4eAuxiliaryMarkerSingleEnded = 113,
	'''
	XC4e Auxiliary Marker (Single-ended mode).
	'''
	XC6eDedicatedOutput = 114,
	'''
	XC6e Dedicated Output (default).
	'''
	XC6eAuxiliaryMarkerDifferential = 115,
	'''
	XC6e Auxiliary Marker (Differential mode).
	'''
	XC6eAuxiliaryMarkerSingleEnded = 116,
	'''
	XC6e Auxiliary Marker (Single-ended mode).
	'''
	XL5eDedicatedOutput = 117,
	'''
	XL5e Dedicated Output (default).
	'''
	XL5eAuxiliaryMarkerDifferential = 118,
	'''
	XL5e Auxiliary Marker (Differential mode).
	'''
	XL5eAuxiliaryMarkerSingleEnded = 119,
	'''
	XL5e Auxiliary Marker (Single-ended mode).
	'''
	XC2DedicatedOutput = 120,
	'''
	XC2 Dedicated Output (default).
	'''
	XC2eDedicatedOutput = 121,
	'''
	XC2e Dedicated Output (default).
	'''
	XL2eDedicatedOutput = 122,
	'''
	XL2e Dedicated Output (default).
	'''
	XI4DedicatedOutput = 123,
	'''
	XI4 Dedicated Output (default).
	'''
	iXC4DedicatedOutput = 124,
	'''
	iXC4 Dedicated Output (default).
	'''
	iXC4AuxiliaryMarkerDifferential = 125,
	'''
	iXC4 Auxiliary Marker (Differential mode).
	'''
	iXC4AuxiliaryMarkerSingleEnded = 126,
	'''
	iXC4 Auxiliary Marker (Single-ended mode).
	'''
	iXC4eDedicatedOutput = 127,
	'''
	iXC4e Dedicated Output (default).
	'''
	iXC4eAuxiliaryMarkerDifferential = 128,
	'''
	iXC4e Auxiliary Marker (Differential mode).
	'''
	iXC4eAuxiliaryMarkerSingleEnded = 129,
	'''
	iXC4e Auxiliary Marker (Single-ended mode).
	'''
	iXC6eDedicatedOutput = 130,
	'''
	iXC6e Dedicated Output (default).
	'''
	iXC6eAuxiliaryMarkerDifferential = 131,
	'''
	iXC6e Auxiliary Marker (Differential mode).
	'''
	iXC6eAuxiliaryMarkerSingleEnded = 132,
	'''
	iXC6e Auxiliary Marker (Single-ended mode).
	'''
	iXL5eDedicatedOutput = 133,
	'''
	iXL5e Dedicated Output (default).
	'''
	iXL5eAuxiliaryMarkerDifferential = 134,
	'''
	iXL5e Auxiliary Marker (Differential mode).
	'''
	iXL5eAuxiliaryMarkerSingleEnded = 135,
	'''
	iXL5e Auxiliary Marker (Single-ended mode).
	'''
	iXR3None = 136,
	'''
	iXR3 None (default).
	'''
	iXR3PsoOutput1 = 137,
	'''
	iXR3 PSO Output 1.
	'''
	iXR3PsoOutput2 = 138,
	'''
	iXR3 PSO Output 2.
	'''
	iXR3PsoOutput3 = 139,
	'''
	iXR3 PSO Output 3.
	'''
	GI4None = 140,
	'''
	GI4 None (default).
	'''
	GI4LaserOutput0 = 141,
	'''
	GI4 Laser Output 0.
	'''
	iXC2DedicatedOutput = 142,
	'''
	iXC2 Dedicated Output (default).
	'''
	iXC2eDedicatedOutput = 143,
	'''
	iXC2e Dedicated Output (default).
	'''
	iXL2eDedicatedOutput = 144,
	'''
	iXL2e Dedicated Output (default).
	'''
	iXI4DedicatedOutput = 145,
	'''
	iXI4 Dedicated Output (default).
	'''
	FLEXDedicatedOutput = 146,
	'''
	FLEX Dedicated Output (default).
	'''
	iFLEXDedicatedOutput = 147,
	'''
	iFLEX Dedicated Output (default).
	'''
	XA4DedicatedOutput = 148,
	'''
	XA4 Dedicated Output (default).
	'''
	iXA4DedicatedOutput = 149,
	'''
	iXA4 Dedicated Output (default).
	'''

class PsoTransformationFunction(CEnum):
	'''
	Selects the function for the PSO input transformation.
	'''
	_init_ = 'value __doc__',
	None_ = 0,
	'''
	No operation.
	'''
	Average = 1,
	'''
	Average.
	'''
	Sum = 2,
	'''
	Sum.
	'''
	Difference = 3,
	'''
	Difference.
	'''

class AutofocusFocusMode(CEnum):
	'''
	Selects whether autofocus will run in continuous focus mode or single focus mode.
	'''
	_init_ = 'value __doc__',
	Continuous = 0,
	'''
	The autofocus routine runs continuously until you turn off autofocus.
	'''
	Single = 1,
	'''
	The autofocus routine automatically turns off when the input that is specified by the AutofocusInput parameter is within the specified deadband of the AutofocusDeadband parameter.
	'''

class AnalogOutputAxisTrackingItem(CEnum):
	'''
	A controller signal used for analog output axis tracking.
	'''
	_init_ = 'value __doc__',
	PositionCommand = 1,
	'''
	The analog output will track the Position Command item in user units.
	'''
	PositionFeedback = 2,
	'''
	The analog output will track the Position Feedback item in user units.
	'''
	VelocityCommand = 3,
	'''
	The analog output will track the Velocity Command item in user units per second.
	'''
	VelocityFeedback = 4,
	'''
	The analog output will track the Velocity Feedback item in user units per second.
	'''
	CurrentCommand = 5,
	'''
	The analog output will track the Current Command item in amps.
	'''
	CurrentFeedback = 6,
	'''
	The analog output will track the Current Feedback item in amps.
	'''
	AccelerationCommand = 7,
	'''
	The analog output will track the Acceleration Command item in user units per second squared.
	'''
	PositionError = 8,
	'''
	The analog output will track the Position Error item in user units.
	'''
	PiezoVoltageCommand = 9,
	'''
	The analog output will track the Piezo Voltage Command item in volts.
	'''
	VectorSpeedCommand = 10,
	'''
	The analog output will track the vector speed in user units per second.
	'''

class AnalogOutputVectorTrackingItem(CEnum):
	'''
	A controller signal used for analog output vector tracking.
	'''
	_init_ = 'value __doc__',
	PositionCommand = 0,
	'''
	The analog output will track the Position Command item in primary units.
	'''
	PositionFeedback = 1,
	'''
	The analog output will track the Position Feedback item in primary units.
	'''
	VelocityCommand = 2,
	'''
	The analog output will track the Velocity Command item in primary units per second.
	'''
	VelocityFeedback = 3,
	'''
	The analog output will track the Velocity Feedback item in primary units per second.
	'''

class ModbusRegisterDataType(CEnum):
	'''
	Specifies the type of the Modbus register.
	'''
	_init_ = 'value __doc__',
	Bit = 1,
	'''
	Represents a 1-bit boolean Modbus register value.
	'''
	Float32 = 2,
	'''
	Represents a 32-bit floating-point Modbus register value.
	'''
	Float64 = 3,
	'''
	Represents a 64-bit floating-point Modbus register value.
	'''
	UInt8 = 4,
	'''
	Represents an 8-bit unsigned integer Modbus register value.
	'''
	UInt16 = 5,
	'''
	Represents a 16-bit unsigned integer Modbus register value.
	'''
	UInt32 = 6,
	'''
	Represents a 32-bit unsigned integer Modbus register value.
	'''
	Int8 = 8,
	'''
	Represents an 8-bit signed integer Modbus register value.
	'''
	Int16 = 9,
	'''
	Represents a 16-bit signed integer Modbus register value.
	'''
	Int32 = 10,
	'''
	Represents a 32-bit signed integer Modbus register value.
	'''

class EthercatRegisterDataType(CEnum):
	'''
	Specifies the type of the EtherCAT register.
	'''
	_init_ = 'value __doc__',
	Bit = 1,
	'''
	Represents a 1-bit boolean EtherCAT register value.
	'''
	Float32 = 2,
	'''
	Represents a 32-bit floating-point EtherCAT register value.
	'''
	Float64 = 3,
	'''
	Represents a 64-bit floating-point EtherCAT register value.
	'''
	UInt8 = 4,
	'''
	Represents an 8-bit unsigned integer EtherCAT register value.
	'''
	UInt16 = 5,
	'''
	Represents a 16-bit unsigned integer EtherCAT register value.
	'''
	UInt32 = 6,
	'''
	Represents a 32-bit unsigned integer EtherCAT register value.
	'''
	Int8 = 8,
	'''
	Represents an 8-bit signed integer EtherCAT register value.
	'''
	Int16 = 9,
	'''
	Represents a 16-bit signed integer EtherCAT register value.
	'''
	Int32 = 10,
	'''
	Represents a 32-bit signed integer EtherCAT register value.
	'''

class EtherNetIpRegisterDataType(CEnum):
	'''
	Specifies the type of the EtherNet/IP register.
	'''
	_init_ = 'value __doc__',
	Bit = 1,
	'''
	Represents a 1-bit boolean EtherNet/IP register value.
	'''
	Float32 = 2,
	'''
	Represents a 32-bit floating-point EtherNet/IP register value.
	'''
	Float64 = 3,
	'''
	Represents a 64-bit floating-point EtherNet/IP register value.
	'''
	UInt8 = 4,
	'''
	Represents an 8-bit unsigned integer EtherNet/IP register value.
	'''
	UInt16 = 5,
	'''
	Represents a 16-bit unsigned integer EtherNet/IP register value.
	'''
	UInt32 = 6,
	'''
	Represents a 32-bit unsigned integer EtherNet/IP register value.
	'''
	Int8 = 8,
	'''
	Represents an 8-bit signed integer EtherNet/IP register value.
	'''
	Int16 = 9,
	'''
	Represents a 16-bit signed integer EtherNet/IP register value.
	'''
	Int32 = 10,
	'''
	Represents a 32-bit signed integer EtherNet/IP register value.
	'''

class EtherNetIpRegisterType(CEnum):
	'''
	The available register sets of an EtherNet/IP Adapter connection.
	'''
	_init_ = 'value __doc__',
	InputBlock0 = 0,
	'''
	496 byte block for input - target to originator (T2O) data.
	'''
	InputBlock1 = 1,
	'''
	496 byte block for input - target to originator (T2O) data.
	'''
	OutputBlock0 = 2,
	'''
	496 byte block for output - originator to target (O2T) data.
	'''
	OutputBlock1 = 3,
	'''
	496 byte block for output - originator to target (O2T) data.
	'''

class DataCollectionFileType(CEnum):
	'''
	Represents a data collection file type.
	'''
	_init_ = 'value __doc__',
	Plt = 0,
	'''
	The Automation1 Plot file type.
	'''
	Csv = 1,
	'''
	The CSV file type.
	'''
	Json = 2,
	'''
	The JSON file type.
	'''

class FrequencyResponseFileType(CEnum):
	'''
	Represents a frequency response file type.
	'''
	_init_ = 'value __doc__',
	Fr = 0,
	'''
	The Automation1 Frequency Response file type.
	'''
	Csv = 1,
	'''
	The CSV file type.
	'''
	Json = 2,
	'''
	The JSON file type.
	'''

class TaskState(CEnum):
	'''
	This value represents information about the state of this task.
	'''
	_init_ = 'value __doc__',
	Unavailable = 0,
	'''
	The Controller Plus Option is not installed. You cannot use this task.
	'''
	Inactive = 1,
	'''
	This task was disabled by the EnabledTasks parameter.
	'''
	Idle = 2,
	'''
	No program is associated or running.
	'''
	ProgramReady = 3,
	'''
	A program is associated but not running.
	'''
	ProgramRunning = 4,
	'''
	A program is associated and running.
	'''
	ProgramFeedhold = 5,
	'''
	A program is associated, was run, and feedhold is active. This state is active from the moment the motion begins to decelerate due to a feedhold until the moment the motion begins to accelerate back to speed due to a feedhold release.
	'''
	ProgramPaused = 6,
	'''
	A program is associated, was run, and was paused.
	'''
	ProgramComplete = 7,
	'''
	A program is associated, was run, and completed.(1)
	'''
	Error = 8,
	'''
	A task error occurred on this task.
	'''
	QueueRunning = 9,
	'''
	This task has an active command queue that is currently running.
	'''
	QueuePaused = 10,
	'''
	This task has an active command queue that is currently paused.
	'''

class MotorType(CEnum):
	'''
	Represents the motor type
	'''
	_init_ = 'value __doc__',
	ACBrushlessLinear = 0,
	'''
	AC Brushless Linear
	'''
	ACBrushlessRotary = 1,
	'''
	AC Brushless Rotary
	'''
	DCBrush = 2,
	'''
	DC Brush
	'''
	StepperMotor = 3,
	'''
	Stepper Motor
	'''
	ThreePhaseStepper = 4,
	'''
	Three Phase Stepper
	'''
	TwoPhaseACBrushless = 6,
	'''
	2-Phase AC Brushless
	'''
	PiezoActuator = 8,
	'''
	Piezo Actuator
	'''
	Galvo = 9,
	'''
	Galvo
	'''

class HomeType(CEnum):
	'''
	Represents the home type
	'''
	_init_ = 'value __doc__',
	PastLimittoMarker = 0,
	'''
	Home Past Limit to Marker
	'''
	ToLimitandReversetoMarker = 1,
	'''
	Home to Limit and Reverse to Marker
	'''
	ToMarkerOnly = 2,
	'''
	Home to Marker Only
	'''
	ToLimitOnly = 3,
	'''
	Home to Limit Only
	'''
	AtCurrentPosition = 4,
	'''
	Home at Current Position
	'''
	AtCurrentPositionFeedback = 5,
	'''
	Home at Current Position Feedback
	'''
	AtCurrentPositionAbsolute = 6,
	'''
	Home at Current Position Absolute
	'''

class PrimaryFeedbackType(CEnum):
	'''
	Represents the feedback type on the primary connector
	'''
	_init_ = 'value __doc__',
	None_ = 0,
	'''
	None
	'''
	IncrementalEncoderSquareWave = 1,
	'''
	Incremental Encoder (Square-Wave)
	'''
	IncrementalEncoderSineWave = 2,
	'''
	Incremental Encoder (Sine-Wave)
	'''
	AbsoluteEncoderEnDatwithSineWaveIncremental = 3,
	'''
	Absolute Encoder (EnDat with Sine-Wave Incremental)
	'''
	AbsoluteEncoderEnDat = 4,
	'''
	Absolute Encoder (EnDat)
	'''
	HallEffectSwitches = 5,
	'''
	Hall-Effect Switches
	'''
	AbsoluteEncoderSSI = 6,
	'''
	Absolute Encoder (SSI)
	'''
	AbsoluteEncoderBiSS = 9,
	'''
	Absolute Encoder (BiSS)
	'''
	AbsoluteEncoderBiSSwithSineWaveIncremental = 10,
	'''
	Absolute Encoder (BiSS with Sine-Wave Incremental)
	'''
	CapacitanceSensor = 11,
	'''
	Capacitance Sensor
	'''

class AuxiliaryFeedbackType(CEnum):
	'''
	Represents the feedback type on the auxiliary connector
	'''
	_init_ = 'value __doc__',
	None_ = 0,
	'''
	None
	'''
	IncrementalEncoderSquareWave = 1,
	'''
	Incremental Encoder (Square-Wave)
	'''
	IncrementalEncoderSineWave = 2,
	'''
	Incremental Encoder (Sine-Wave)
	'''
	AbsoluteEncoderEnDat = 4,
	'''
	Absolute Encoder (EnDat)
	'''
	AbsoluteEncoderSSI = 6,
	'''
	Absolute Encoder (SSI)
	'''
	AbsoluteEncoderBiSS = 9,
	'''
	Absolute Encoder (BiSS)
	'''

class PiezoDefaultServoState(CEnum):
	'''
	Represents the piezo default servo state.
	'''
	_init_ = 'value __doc__',
	Off = 0,
	'''
	Servo Off
	'''
	On = 1,
	'''
	Servo On
	'''

class PsoStatus(CEnum):
	'''
	Represents PSO status
	'''
	_init_ = 'value __doc__',
	WaveformActive = 1 << 4,
	'''
	The Waveform module is actively generating a waveform.
	'''
	BitOutputActive = 1 << 5,
	'''
	The state of the Bit module output.
	'''
	Window1OutputActive = 1 << 6,
	'''
	The state of the Window 1 module output.
	'''
	Window2OutputActive = 1 << 7,
	'''
	The state of the Window 2 module output.
	'''
	OutputActive = 1 << 10,
	'''
	The state of the Output module output.
	'''
	ExternalSyncInput = 1 << 11,
	'''
	The state of the external synchronization input that is used with the PsoPulseExternalSyncOn function.
	'''
	DistanceArrayDepleted = 1 << 12,
	'''
	The Distance module attempted to load a new array mode distance when no new distance values were available. The distance counters are disabled until new distance values are specified.
	'''
	Window1ArrayDepleted = 1 << 13,
	'''
	The Window 1 module attempted to load a new array mode window range when no new range values were available. The window output is disabled until new range values are specified.
	'''
	Window2ArrayDepleted = 1 << 14,
	'''
	The Window 2 module attempted to load a new array mode window range when no new range values were available. The window output is disabled until new range values are specified.
	'''
	BitArrayDepleted = 1 << 15,
	'''
	The Bit module attempted to load a new bit value when no new bit values were available. The bit output is disabled until new range values are specified.
	'''
	WaveformArrayDepleted = 1 << 16,
	'''
	The Waveform module attempted to load a new array mode parameter value when no new parameter values were available. The waveform module is disabled until new parameter values are specified.
	'''
	DistanceFifoEmpty = 1 << 0,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been obsoleted by DistanceArrayDepleted. Use DistanceArrayDepleted instead of this enum value.
	'''
	LaserFifoEmpty = 1 << 1,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been obsoleted by WaveformArrayDepleted. Use WaveformArrayDepleted instead of this enum value.
	'''
	Window1FifoEmpty = 1 << 2,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been obsoleted by Window1ArrayDepleted. Use Window1ArrayDepleted instead of this enum value.
	'''
	Window2FifoEmpty = 1 << 3,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been obsoleted by Window2ArrayDepleted. Use Window2ArrayDepleted instead of this enum value.
	'''
	FiringActivePulseGen1 = 1 << 4,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been obsoleted by WaveformActive. Use WaveformActive instead of this enum value.
	'''
	FiringActivePulseGenerator1 = 1 << 4,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been obsoleted by WaveformActive. Use WaveformActive instead of this enum value.
	'''
	FiringActivePulseGen2 = 1 << 5,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been removed because the feature does not exist in Automation1. This bit is now used for BitOutputActive.
	'''
	FiringActivePulseGenerator2 = 1 << 5,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been removed because the feature does not exist in Automation1. This bit is now used for BitOutputActive.
	'''
	InsideWindow1 = 1 << 6,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to Window1OutputActive. Use Window1OutputActive instead of this enum value.
	'''
	InsideWindow2 = 1 << 7,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to Window2OutputActive. Use Window2OutputActive instead of this enum value.
	'''
	PsoInterlock = 1 << 8,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been removed because the feature does not exist in Automation1.
	'''
	PsoOutput1Status = 1 << 9,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been obsoleted by OutputActive. Use OutputActive instead of this enum value.
	'''
	PsoOutput2Status = 1 << 10,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been removed because the feature does not exist in Automation1. This bit is now used for OutputActive.
	'''
	PsoExtSync = 1 << 11,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to ExternalSyncInput. Use ExternalSyncInput instead of this enum value.
	'''
	PsoExternalSyncInput = 1 << 11,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to ExternalSyncInput. Use ExternalSyncInput instead of this enum value.
	'''

class StoStatus(CEnum):
	'''
	Represents the Safe Torque Off (STO) status for an axis.
	'''
	_init_ = 'value __doc__',
	Sto1Activated = 1 << 0,
	'''
	Safe Torque Off (STO) channel 1 hardware is activated and preventing torque.
	'''
	Sto1Event = 1 << 1,
	'''
	Power has been removed from the Safe Torque Off (STO) channel 1 input. Torque on the motor will be prevented after the hardware time delay.
	'''
	Sto2Activated = 1 << 2,
	'''
	Safe Torque Off (STO) channel 2 hardware is activated and preventing torque.
	'''
	Sto2Event = 1 << 3,
	'''
	Power has been removed from the Safe Torque Off (STO) channel 2 input. Torque on the motor will be prevented after the hardware time delay.
	'''
	StoCrossCheckFault = 1 << 4,
	'''
	The Safe Torque Off (STO) diagnostic check has detected a hardware problem on an STO channel and is preventing torque on the motor.
	'''

class BissStatus(CEnum):
	'''
	Represents the BiSS status for a feedback input.
	'''
	_init_ = 'value __doc__',
	CrcError = 1 << 0,
	'''
	A CRC error occurred while the drive communicated with the encoder.
	'''
	EncoderWarning = 1 << 1,
	'''
	The warning bit from the encoder is active.
	'''
	EncoderError = 1 << 2,
	'''
	The error bit from the encoder is active.
	'''
	TimeoutError = 1 << 3,
	'''
	The encoder did not respond in the necessary time interval.
	'''

class AxisStatus(CEnum):
	'''
	Represents an axis status
	'''
	_init_ = 'value __doc__',
	Homed = 1 << 0,
	'''
	The axis is homed.
	'''
	Profiling = 1 << 1,
	'''
	The axis is performing coordinated (LINEAR, CW, CCW, BEZIER), RAPID, or PVT motion.
	'''
	WaitDone = 1 << 2,
	'''
	The controller finished waiting for motion on this axis to complete. The behavior of this bit depends on the selected wait mode. When in Wait Mode Motion Done, this bit will mimic the Motion Done bit, but when in Wait Mode In Position, this bit will not be active until both the Motion Done bit and the In Position bit are both active.
	'''
	CommandValid = 1 << 3,
	'''
	Motion on the axis is controlled from the SMC.
	'''
	Homing = 1 << 4,
	'''
	The axis is currently homing.
	'''
	Enabling = 1 << 5,
	'''
	The axis is currently enabling.
	'''
	JogGenerating = 1 << 7,
	'''
	This bit represents internal status.
	'''
	Jogging = 1 << 8,
	'''
	The axis is performing asynchronous motion (MoveIncremental(), MoveAbsolute(), MoveFreerun()).
	'''
	DrivePending = 1 << 9,
	'''
	The SMC sent a command to the drive that will cause the drive to take control of the motion, but the drive has not yet done so.
	'''
	DriveAbortPending = 1 << 10,
	'''
	The SMC sent an abort command to the drive, but the drive has not yet started the abort.
	'''
	TrajectoryFiltering = 1 << 11,
	'''
	Trajectory filtering is enabled for this axis using either the TrajectoryIIRFilter or TrajectoryFIRFilter parameters.
	'''
	IfovEnabled = 1 << 12,
	'''
	Infinite Field of View (IFOV) is enabled for this axis. Enable IFOV by issuing the IFOV ON command. Disable IFOV by issuing the IFOV OFF command.
	'''
	NotVirtual = 1 << 13,
	'''
	A physical drive is associated with this axis. Axes with no drive attached will clear this bit and operate as virtual axes.
	'''
	CalibrationEnabled1D = 1 << 14,
	'''
	The specified 1D calibration file contains a calibration table that corrects this axis. The state of this bit is not affected by the CALENABLE or CALDISABLE commands.
	'''
	CalibrationEnabled2D = 1 << 15,
	'''
	The specified 2D calibration file contains a calibration table that corrects this axis. The state of this bit is not affected by the CALENABLE or CALDISABLE commands.
	'''
	CammingGearingControl = 1 << 16,
	'''
	The axis is currently controlled by camming or gearing.
	'''
	JoystickControl = 1 << 17,
	'''
	The axis is currently performing motion under control of the JOYSTICK command.
	'''
	BacklashActive = 1 << 18,
	'''
	Backlash compensation is enabled for this axis using the BacklashDistance parameter or the BACKLASH ON command.
	'''
	GainMappingEnabled = 1 << 19,
	'''
	A Gain Mapping table was specified for this axis.
	'''
	TransformationInput = 1 << 20,
	'''
	The motion on this axis is the input to a kinematic transformation.
	'''
	TransformationOutput = 1 << 21,
	'''
	The motion on this axis is the output of a kinematic transformation.
	'''
	MotionDone = 1 << 22,
	'''
	Motion on this axis is done, meaning that the velocity command reached zero.
	'''
	MotionClamped = 1 << 23,
	'''
	Motion on this axis is being clamped due to a software limit clamp or safe zone. Refer to the SoftwareLimitSetup parameter, and the Safe zone overview.
	'''
	GantryAligned = 1 << 24,
	'''
	This axis is part of a gantry pair and the gantry is correctly aligned. This bit will not be active until the gantry axes have been homed.
	'''
	GantryDriveControlRealigning = 1 << 25,
	'''
	The axis is currently performing gantry realignment motion due to Theta axis misalignment caused by drive motion.
	'''
	ThermoCompEnabled = 1 << 27,
	'''
	The ThermoComp feature is currently turned on.
	'''
	CalEnabled1D = 1 << 14,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CalibrationEnabled1D. Use CalibrationEnabled1D instead of this enum value.
	'''
	CalEnabled2D = 1 << 15,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CalibrationEnabled2D. Use CalibrationEnabled2D instead of this enum value.
	'''

class AxisFault(CEnum):
	'''
	Represents the faults of an axis
	'''
	_init_ = 'value __doc__',
	PositionErrorFault = 1 << 0,
	'''
	The absolute value of the difference between the position command and the position feedback exceeded the threshold specified by the PositionErrorThreshold parameter.
	'''
	OverCurrentFault = 1 << 1,
	'''
	The average motor current exceeded the threshold specified by the AverageCurrentThreshold and AverageCurrentTime parameters.
	'''
	CwEndOfTravelLimitFault = 1 << 2,
	'''
	The axis encountered the clockwise (positive) end-of-travel limit switch.
	'''
	CcwEndOfTravelLimitFault = 1 << 3,
	'''
	The axis encountered the counter-clockwise (negative) end-of-travel limit switch.
	'''
	CwSoftwareLimitFault = 1 << 4,
	'''
	The axis was commanded to move beyond the position specified by the SoftwareLimitHigh parameter.
	'''
	CcwSoftwareLimitFault = 1 << 5,
	'''
	The axis was commanded to move beyond the position specified by the SoftwareLimitLow parameter.
	'''
	AmplifierFault = 1 << 6,
	'''
	The amplifier for this axis exceeded its maximum current rating or experienced an internal error.
	'''
	FeedbackInput0Fault = 1 << 7,
	'''
	The drive detected a problem with the feedback device specified by the FeedbackInput0 parameter. Or, the drive detected an invalid feedback configuration.
	'''
	FeedbackInput1Fault = 1 << 8,
	'''
	The drive detected a problem with the feedback device specified by the FeedbackInput1 parameter. Or, the drive detected an invalid feedback configuration.
	'''
	HallSensorFault = 1 << 9,
	'''
	The drive detected an invalid state (all high or all low) for the Hall-effect sensor inputs on this axis.
	'''
	MaxVelocityCommandFault = 1 << 10,
	'''
	The commanded velocity is more than the velocity command threshold. Before the axis is homed, this threshold is specified by the VelocityCommandThresholdBeforeHome parameter. After the axis is homed, this threshold is specified by the VelocityCommandThreshold parameter.
	'''
	EmergencyStopFault = 1 << 11,
	'''
	The emergency stop sense input, specified by the ESTOPFaultInput or SoftwareESTOPInput parameter, was triggered, or the controller detected a fault condition in the Safe Torque Off (STO) hardware.
	'''
	VelocityErrorFault = 1 << 12,
	'''
	The absolute value of the difference between the velocity command and the velocity feedback exceeded the threshold specified by the VelocityErrorThreshold parameter.
	'''
	CommutationFault = 1 << 13,
	'''
	The axis attempted commutation, but could not initialize correctly.
	'''
	ExternalFault = 1 << 15,
	'''
	The external fault input, specified by the ExternalFaultAnalogInput, ExternalFaultDigitalInput, or SoftwareExternalFaultInput parameter, was triggered.
	'''
	MotorTemperatureFault = 1 << 17,
	'''
	The motor thermistor input was triggered, which indicates that the motor exceeded its maximum recommended operating temperature.
	'''
	AmplifierTemperatureFault = 1 << 18,
	'''
	The amplifier temperature is not within the operating range or the shunt resistor temperature has exceeded the maximum threshold. This fault occurs at amplifier temperatures less than 0° C or greater than 75° C and shunt resistor temperatures greater than 200° C.
	'''
	EncoderFault = 1 << 19,
	'''
	The encoder fault input on the motor feedback connector was triggered.
	'''
	GantryMisalignmentFault = 1 << 22,
	'''
	The position command or position feedback of the rotary gantry axis exceeded the value specified by the GantryMisalignmentThreshold parameter.
	'''
	FeedbackScalingFault = 1 << 23,
	'''
	The difference between the position feedback and the scaled (adjusted by GainKv) velocity feedback exceeds the threshold specified by the PositionErrorThreshold parameter.
	'''
	MarkerSearchFault = 1 << 24,
	'''
	The distance that the axis moved while searching for the marker exceeded the threshold specified by the MarkerSearchThreshold parameter.
	'''
	SafeZoneFault = 1 << 25,
	'''
	The axis decelerated to a stop because the motion violated a safe zone.
	'''
	InPositionTimeoutFault = 1 << 26,
	'''
	The axis did not achieve in position status in the period specified by the InPositionDisableTimeout parameter.
	'''
	VoltageClampFault = 1 << 27,
	'''
	The commanded voltage output exceeded the value of the PiezoVoltageClampLow or PiezoVoltageClampHigh parameter.
	'''
	MotorSupplyFault = 1 << 28,
	'''
	The amplifier detected that no motor supply voltage is present or that the motor supply voltage is less than the minimum required voltage.
	'''
	InternalFault = 1 << 30,
	'''
	The drive encountered an internal error that caused it to disable. Contact Aerotech Global Technical Support.
	'''
	PositionError = 1 << 0,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to PositionErrorFault. Use PositionErrorFault instead of this enum value.
	'''
	OverCurrent = 1 << 1,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to OverCurrentFault. Use OverCurrentFault instead of this enum value.
	'''
	CwEotLimit = 1 << 2,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CwEndOfTravelLimitFault. Use CwEndOfTravelLimitFault instead of this enum value.
	'''
	CcwEotLimit = 1 << 3,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CcwEndOfTravelLimitFault. Use CcwEndOfTravelLimitFault instead of this enum value.
	'''
	CwSoftLimit = 1 << 4,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CwSoftwareLimitFault. Use CwSoftwareLimitFault instead of this enum value.
	'''
	CcwSoftLimit = 1 << 5,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CcwSoftwareLimitFault. Use CcwSoftwareLimitFault instead of this enum value.
	'''
	FbkInput0 = 1 << 7,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to FeedbackInput0Fault. Use FeedbackInput0Fault instead of this enum value.
	'''
	FbkInput1 = 1 << 8,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to FeedbackInput1Fault. Use FeedbackInput1Fault instead of this enum value.
	'''
	HallFault = 1 << 9,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to HallSensorFault. Use HallSensorFault instead of this enum value.
	'''
	MaxVelocity = 1 << 10,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to MaxVelocityCommandFault. Use MaxVelocityCommandFault instead of this enum value.
	'''
	EstopFault = 1 << 11,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to EmergencyStopFault. Use EmergencyStopFault instead of this enum value.
	'''
	VelocityError = 1 << 12,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to VelocityErrorFault. Use VelocityErrorFault instead of this enum value.
	'''
	MotorTemp = 1 << 17,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to MotorTemperatureFault. Use MotorTemperatureFault instead of this enum value.
	'''
	AmplifierTemp = 1 << 18,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to AmplifierTemperatureFault. Use AmplifierTemperatureFault instead of this enum value.
	'''
	MisalignmentFault = 1 << 22,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to GantryMisalignmentFault. Use GantryMisalignmentFault instead of this enum value.
	'''
	FbkScalingFault = 1 << 23,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to FeedbackScalingFault. Use FeedbackScalingFault instead of this enum value.
	'''
	MrkSearchFault = 1 << 24,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to MarkerSearchFault. Use MarkerSearchFault instead of this enum value.
	'''
	InPosTimeout = 1 << 26,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to InPositionTimeoutFault. Use InPositionTimeoutFault instead of this enum value.
	'''
	VoltageClamp = 1 << 27,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to VoltageClampFault. Use VoltageClampFault instead of this enum value.
	'''
	MotorSupply = 1 << 28,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to MotorSupplyFault. Use MotorSupplyFault instead of this enum value.
	'''
	Internal = 1 << 30,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to InternalFault. Use InternalFault instead of this enum value.
	'''

class DriveStatus(CEnum):
	'''
	Represents the drive status bits
	'''
	_init_ = 'value __doc__',
	Enabled = 1 << 0,
	'''
	The axis is enabled.
	'''
	CwEndOfTravelLimitInput = 1 << 1,
	'''
	This represents the state of the CW end of travel limit input. It is affected by the active polarity, which is configured by the EndOfTravelLimitSetup parameter.
	'''
	CcwEndOfTravelLimitInput = 1 << 2,
	'''
	This represents the state of the CCW end of travel limit input. It is affected by the active polarity, which is configured by the EndOfTravelLimitSetup parameter.
	'''
	HomeLimitInput = 1 << 3,
	'''
	This represents the state of the home limit input. It is affected by the active polarity, which is configured by the EndOfTravelLimitSetup parameter.
	'''
	MarkerInput = 1 << 4,
	'''
	This represents the state of the marker input.
	'''
	HallAInput = 1 << 5,
	'''
	This represents the state of the Hall-effect sensor A input.
	'''
	HallBInput = 1 << 6,
	'''
	This represents the state of the Hall-effect sensor B input.
	'''
	HallCInput = 1 << 7,
	'''
	This represents the state of the Hall-effect sensor C input.
	'''
	SineEncoderError = 1 << 8,
	'''
	An error condition is present on the Sine encoder input of the position feedback device.
	'''
	CosineEncoderError = 1 << 9,
	'''
	An error condition is present on the Cosine encoder input of the position feedback device.
	'''
	EmergencyStopInput = 1 << 10,
	'''
	This represents the state of the emergency stop sense input.
	'''
	BrakeOutput = 1 << 11,
	'''
	State of the dedicated brake output.
	'''
	GalvoPowerCorrection = 1 << 12,
	'''
	Galvo Power Correction is configured on this axis.
	'''
	AmplifierActive = 1 << 13,
	'''
	The amplifier associated with this physical axis is active and outputting current to the attached motor.
	'''
	NoMotorSupply = 1 << 14,
	'''
	The drive detected that no motor supply voltage is present.
	'''
	CurrentClamp = 1 << 15,
	'''
	For piezo drives, the controller clamps the motor output to the value of the PiezoVoltageClampLow or the PiezoVoltageClampHigh parameter. For all other drives, the controller clamps the motor output to the value of the MaxCurrentClamp parameter.
	'''
	MarkerLatch = 1 << 16,
	'''
	The position of the marker is latched.
	'''
	PowerLimiting = 1 << 17,
	'''
	The motor output is being limited to prevent damage to the amplifier.
	'''
	GalvoCalibrationEnabled = 1 << 20,
	'''
	The specified 2D calibration file contains a galvo calibration table that corrects this axis.
	'''
	AutofocusActive = 1 << 21,
	'''
	The axis is operating under control of the AUTOFOCUS loop.
	'''
	ProgrammingFlash = 1 << 22,
	'''
	The drive is programming its internal flash memory.
	'''
	ServoControl = 1 << 24,
	'''
	The axis is operating under servo control.
	'''
	InPosition = 1 << 25,
	'''
	The axis is considered to be in position as configured by the InPositionDistance and InPositionTime parameters.
	'''
	MoveActive = 1 << 26,
	'''
	The axis is performing drive generated motion.
	'''
	AccelerationPhase = 1 << 27,
	'''
	The axis is accelerating.
	'''
	DecelerationPhase = 1 << 28,
	'''
	The axis is decelerating.
	'''
	EncoderClipping = 1 << 29,
	'''
	The on-board encoder multiplier detected that the input signals may be exceeding the maximum input range, which results in clipping of the encoder signals.
	'''
	DualLoopActive = 1 << 30,
	'''
	The axis is operating in dual-loop mode using two different feedback devices.
	'''
	CwEotLimit = 1 << 1,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CwEndOfTravelLimitInput. Use CwEndOfTravelLimitInput instead of this enum value.
	'''
	CcwEotLimit = 1 << 2,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CcwEndOfTravelLimitInput. Use CcwEndOfTravelLimitInput instead of this enum value.
	'''
	HomeLimit = 1 << 3,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to HomeLimitInput. Use HomeLimitInput instead of this enum value.
	'''
	EstopInput = 1 << 10,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to EmergencyStopInput. Use EmergencyStopInput instead of this enum value.
	'''
	GalvoCalEnabled = 1 << 20,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to GalvoCalibrationEnabled. Use GalvoCalibrationEnabled instead of this enum value.
	'''
	ProgramFlash = 1 << 22,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to ProgrammingFlash. Use ProgrammingFlash instead of this enum value.
	'''
	AccelPhase = 1 << 27,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to AccelerationPhase. Use AccelerationPhase instead of this enum value.
	'''
	DecelPhase = 1 << 28,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to DecelerationPhase. Use DecelerationPhase instead of this enum value.
	'''

class TaskStatus0(CEnum):
	'''
	Represents a set of task status
	'''
	_init_ = 'value __doc__',
	ProgramAssociated = 1 << 0,
	'''
	A program is associated with this task.
	'''
	ImmediateExecuting = 1 << 3,
	'''
	An immediate command is executing.
	'''
	ReturnMotionExecuting = 1 << 4,
	'''
	Return motion is executing due to an TaskInterruptMotionOff() function.
	'''
	ProgramReset = 1 << 8,
	'''
	The program is reset.
	'''
	PendingAxesStop = 1 << 9,
	'''
	One or more axes are decelerating due to an abort, task stop, task error, feedhold, onerror, or retrace direction reversal that occurs during a RAPID, LINEAR, CW, CCW, or BEZIER motion.
	'''
	FeedholdActive = 1 << 11,
	'''
	Bit turns on as soon as motion begins to decelerate due to a feedhold. Bit turns off when motion begins to accelerate back to speed due to a feedhold release. The FeedholdAxesStopped bit of Task Status 1 indicates when deceleration due to a feedhold stops.
	'''
	CallbackHoldActive = 1 << 12,
	'''
	A callback command was issued and is waiting for a front-end application to acknowledge the command.
	'''
	CallbackResponding = 1 << 13,
	'''
	A callback command was issued and is waiting for a front-end application to handle the command.
	'''
	SpindleActive = 1 << 14,
	'''
	The spindle is currently active.
	'''
	Retrace = 1 << 19,
	'''
	Retrace is active.
	'''
	InterruptMotionActive = 1 << 21,
	'''
	Interrupt motion is active.
	'''
	JoystickActive = 1 << 22,
	'''
	The task is executing a JoystickRun() function.
	'''
	CornerRounding = 1 << 23,
	'''
	Corner rounding is enabled.
	'''
	JoystickLowSpeedActive = 1 << 25,
	'''
	The joystick is using the low speed mode.
	'''
	SynchronizedFunctionExecuting = 1 << 27,
	'''
	A synchronized function is executing.
	'''
	TaskControlRestricted = 1 << 29,
	'''
	The task has control restrictions enabled.
	'''
	SyncFunctionExecuting = 1 << 27,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to SynchronizedFunctionExecuting. Use SynchronizedFunctionExecuting instead of this enum value.
	'''

class TaskStatus1(CEnum):
	'''
	Represents a set of task status
	'''
	_init_ = 'value __doc__',
	AsyncSmcMotionAbortPending = 1 << 1,
	'''
	An asynchronous motion is aborting.
	'''
	RetraceRequested = 1 << 3,
	'''
	A retrace operation was requested.
	'''
	MsoChange = 1 << 4,
	'''
	An MSO change was issued.
	'''
	SpindleFeedhold = 1 << 5,
	'''
	A spindle is in feedhold.
	'''
	FeedholdAxesStopped = 1 << 6,
	'''
	Bit turns on as soon as deceleration due to a feedhold ends. Bit turns off when motion begins to accelerate back to speed due to a feedhold release. The FeedholdActive bit of Task Status 0 indicates when a feedhold is issued.
	'''
	CutterRadiusEnabling = 1 << 7,
	'''
	Cutter radius compensation is performing a lead-on move.
	'''
	CutterRadiusDisabling = 1 << 8,
	'''
	Cutter radius compensation is performing a lead-off move.
	'''
	CutterOffsetsEnablingPositive = 1 << 9,
	'''
	Cutter offset compensation is performing a lead-on positive move.
	'''
	CutterOffsetsEnablingNegative = 1 << 10,
	'''
	Cutter offset compensation is performing a lead-on negative move.
	'''
	CutterOffsetsDisabling = 1 << 11,
	'''
	Cutter offset compensation is performing a lead-off move.
	'''
	OnErrorHandlerPending = 1 << 13,
	'''
	An onerror handler is pending.
	'''
	OnErrorHandlerExecuting = 1 << 14,
	'''
	An onerror handler is executing.
	'''
	ProgramStopPending = 1 << 16,
	'''
	A program stop is pending.
	'''
	SynchronizedFunctionPending = 1 << 17,
	'''
	A synchronized function is pending.
	'''
	NoMfoFloor = 1 << 18,
	'''
	The MfoMinimum parameter is negative.
	'''
	Interrupted = 1 << 19,
	'''
	This bit represents internal status.
	'''
	IfovBufferHold = 1 << 25,
	'''
	This bit represents internal status.
	'''
	CutterOffsetsEnablingPos = 1 << 9,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CutterOffsetsEnablingPositive. Use CutterOffsetsEnablingPositive instead of this enum value.
	'''
	CutterOffsetsEnablingNeg = 1 << 10,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CutterOffsetsEnablingNegative. Use CutterOffsetsEnablingNegative instead of this enum value.
	'''
	SyncFunctionPending = 1 << 17,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to SynchronizedFunctionPending. Use SynchronizedFunctionPending instead of this enum value.
	'''

class TaskStatus2(CEnum):
	'''
	Represents a set of task status
	'''
	_init_ = 'value __doc__',
	ScalingActive = 1 << 3,
	'''
	Parts scaling is active.
	'''
	ProfileActive = 1 << 5,
	'''
	Profile motion is active.
	'''
	MotionModeRapid = 1 << 6,
	'''
	The motion mode is Rapid (G0).
	'''
	MotionModeLinear = 1 << 7,
	'''
	The motion mode is Linear (G1).
	'''
	MotionPvt = 1 << 8,
	'''
	MovePvt() motion is being executed.
	'''
	MotionContinuousActive = 1 << 9,
	'''
	The task is actively velocity profiling.
	'''
	CutterOffsetsActivePositive = 1 << 12,
	'''
	Positive cutter offset compensation is active.
	'''
	CutterRadiusActiveLeft = 1 << 13,
	'''
	Cutter radius compensation left is active.
	'''
	CutterRadiusActiveRight = 1 << 14,
	'''
	Cutter radius compensation right is active.
	'''
	CutterOffsetsActiveNegative = 1 << 15,
	'''
	Negative cutter offset compensation is active.
	'''
	NormalcyActiveLeft = 1 << 16,
	'''
	Normalcy left is active.
	'''
	NormalcyActiveRight = 1 << 17,
	'''
	Normalcy right is active.
	'''
	NormalcyAlignment = 1 << 18,
	'''
	A normalcy alignment move is being performed.
	'''
	MotionModeCw = 1 << 19,
	'''
	The motion mode is CW (G2).
	'''
	MotionModeCcw = 1 << 20,
	'''
	The motion mode is CCW (G3).
	'''
	LimitFeedrateActive = 1 << 21,
	'''
	Feedrate limiting is active.
	'''
	LimitMfoActive = 1 << 22,
	'''
	MFO limiting is active.
	'''
	Coord1Plane1 = 1 << 23,
	'''
	Coordinate System 1 Plane 1 is active.
	'''
	Coord1Plane2 = 1 << 24,
	'''
	Coordinate System 1 Plane 2 is active.
	'''
	Coord1Plane3 = 1 << 25,
	'''
	Coordinate System 1 Plane 3 is active.
	'''
	Coord2Plane1 = 1 << 26,
	'''
	Coordinate System 2 Plane 1 is active.
	'''
	Coord2Plane2 = 1 << 27,
	'''
	Coordinate System 2 Plane 2 is active.
	'''
	Coord2Plane3 = 1 << 28,
	'''
	Coordinate System 2 Plane 3 is active.
	'''
	CutterOffsetsActivePos = 1 << 12,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CutterOffsetsActivePositive. Use CutterOffsetsActivePositive instead of this enum value.
	'''
	CutterOffsetsActiveNeg = 1 << 15,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CutterOffsetsActiveNegative. Use CutterOffsetsActiveNegative instead of this enum value.
	'''

class TaskMode(CEnum):
	'''
	Represents a set of task status
	'''
	_init_ = 'value __doc__',
	Secondary = 1 << 0,
	'''
	Secondary units mode is in use.
	'''
	Absolute = 1 << 1,
	'''
	Absolute programming mode is in use.
	'''
	AccelTypeLinear = 1 << 2,
	'''
	The acceleration type is configured for linear ramping.
	'''
	AccelModeRate = 1 << 3,
	'''
	The acceleration mode is rate-based.
	'''
	InverseDominance = 1 << 4,
	'''
	Inverse dominance (G98) mode is active.
	'''
	MotionContinuous = 1 << 5,
	'''
	Motion continuous (VelocityBlendingOn()) mode is active.
	'''
	SpindleStopOnProgramHalt = 1 << 7,
	'''
	Spindles will abort on a program stop (G101).
	'''
	OptionalPause = 1 << 9,
	'''
	Optional Pause mode is active (G114).
	'''
	AccelTypeSCurve = 1 << 10,
	'''
	The acceleration type is configured for S-curve ramping.
	'''
	MfoLock = 1 << 11,
	'''
	MFO Lock mode is active (M48).
	'''
	MsoLock = 1 << 12,
	'''
	MSO Lock mode is active (M50).
	'''
	DecelTypeLinear = 1 << 13,
	'''
	The deceleration type is configured for linear ramping.
	'''
	DecelTypeSCurve = 1 << 14,
	'''
	The deceleration type is configured for S-curve ramping.
	'''
	ProgramFeedrateInverseTime = 1 << 16,
	'''
	Programmed feed rates are specified in inverse time units (G93).
	'''
	ProgramFeedrateUnitsPerSpindleRev = 1 << 17,
	'''
	Programmed feed rates are specified in units per spindle revolution (G95).
	'''
	DecelModeRate = 1 << 24,
	'''
	The deceleration mode is rate-based.
	'''
	MfoActiveOnJog = 1 << 26,
	'''
	MFO will affect asynchronous motion (G121).
	'''
	WaitForInPos = 1 << 27,
	'''
	The wait for in-position wait mode is active.
	'''
	Minutes = 1 << 28,
	'''
	When this bit is true the time units are minutes. When this bit is false the time units are seconds.
	'''
	WaitAuto = 1 << 30,
	'''
	The automatic wait mode is active.
	'''

class RampType(CEnum):
	'''
	Represents a motion ramping type.
	'''
	_init_ = 'value __doc__',
	Linear = 0,
	'''
	Linear-based acceleration and deceleration.
	'''
	SCurve = 1,
	'''
	S-curve-based acceleration and deceleration.
	'''
	Sine = 2,
	'''
	Sine-based acceleration and deceleration.
	'''

class RampMode(CEnum):
	'''
	Represents a motion ramping mode.
	'''
	_init_ = 'value __doc__',
	Rate = 0,
	'''
	Rate-based acceleration and deceleration.
	'''
	Time = 1,
	'''
	Time-based acceleration and deceleration.
	'''

class ModbusRegisterType(CEnum):
	'''
	The available register sets of a Modbus Client or Modbus Server connection.
	'''
	_init_ = 'value __doc__',
	InputWords = 0,
	'''
	16-bit inputs.
	'''
	OutputWords = 1,
	'''
	16-bit outputs.
	'''
	InputBits = 2,
	'''
	1-bit inputs.
	'''
	OutputBits = 3,
	'''
	1-bit outputs.
	'''
	OutputWordsStatus = 4,
	'''
	Read-only 16-bit outputs.
	'''
	OutputBitsStatus = 5,
	'''
	Read-only 1-bit outputs.
	'''

class EthercatRegisterType(CEnum):
	'''
	The available register sets of an EtherCAT connection which represent the access level to the PDO space.
	'''
	_init_ = 'value __doc__',
	RxPdo = 0,
	'''
	Receive (Rx) Process Data Objects (PDO) packets. Read-Only
	'''
	TxPdo = 1,
	'''
	Transmit (Tx) Process Data Objects (PDO) packets. Read/Write
	'''

class CalibrationType(CEnum):
	'''
	Specifies the type of calibration that will be performed by a calibration action.
	'''
	_init_ = 'value __doc__',
	AxisCalibration1D = 0,
	'''
	1D Axis Calibration.
	'''
	AxisCalibration2D = 1,
	'''
	2D Axis Calibration.
	'''
	Galvo2DAxisCalibration = 2,
	'''
	Galvo 2D Axis Calibration.
	'''
	GalvoPowerCorrection = 3,
	'''
	Galvo Power Correction.
	'''

class FeedbackInput0(CEnum):
	'''
	Represents the first feedback input
	'''
	_init_ = 'value __doc__',
	PositionCommand = 0,
	'''
	Position Command
	'''
	PrimaryFeedback = 1,
	'''
	Primary Feedback
	'''
	AuxiliaryFeedback = 2,
	'''
	Auxiliary Feedback
	'''
	AnalogInput0 = 3,
	'''
	Analog Input 0
	'''
	AnalogInput1 = 4,
	'''
	Analog Input 1
	'''
	AnalogInput2 = 5,
	'''
	Analog Input 2
	'''
	AnalogInput3 = 6,
	'''
	Analog Input 3
	'''

class FeedbackInput1(CEnum):
	'''
	Represents the second feedback input
	'''
	_init_ = 'value __doc__',
	PositionCommand = 0,
	'''
	Position Command
	'''
	PrimaryFeedback = 1,
	'''
	Primary Feedback
	'''
	AuxiliaryFeedback = 2,
	'''
	Auxiliary Feedback
	'''
	AnalogInput0 = 3,
	'''
	Analog Input 0
	'''
	AnalogInput1 = 4,
	'''
	Analog Input 1
	'''
	AnalogInput2 = 5,
	'''
	Analog Input 2
	'''
	AnalogInput3 = 6,
	'''
	Analog Input 3
	'''

class TuningDisturbanceType(CEnum):
	'''
	The type of disturbance to use when measuring a frequency response.
	'''
	_init_ = 'value __doc__',
	Sinusoid = 1,
	'''
	Use a sinusoid disturbance.
	'''
	WhiteNoise = 2,
	'''
	Use a white noise disturbance.
	'''
	DriveArray = 5,
	'''
	Use the drive array to define a custom disturbance.
	'''
	MultisinePlus = 6,
	'''
	Use the MultisinePlus disturbance.
	'''

class TuningMeasurementType(CEnum):
	'''
	The type of frequency response to measure.
	'''
	_init_ = 'value __doc__',
	ServoOpenLoop = 0,
	'''
	Measure the open loop response of the servo loop.
	'''
	CurrentOpenLoop = 2,
	'''
	Measure the open loop response of the current loop.
	'''
	AutoFocusOpenLoop = 3,
	'''
	Measure the open loop response of the auto-focus loop.
	'''

class EnDatStatus(CEnum):
	'''
	Represents the EnDat status for a feedback input.
	'''
	_init_ = 'value __doc__',
	CrcError = 1 << 0,
	'''
	A CRC error occurred while the drive communicated with the encoder.
	'''
	ReceiveError = 1 << 1,
	'''
	The encoder sent a "data receive error".
	'''
	TimeoutError = 1 << 2,
	'''
	The encoder did not respond in the necessary time interval.
	'''

class PrimaryFeedbackStatus(CEnum):
	'''
	Represents the primary feedback connector status bits
	'''
	_init_ = 'value __doc__',
	CwEndOfTravelLimitInput = 1 << 0,
	'''
	This represents the state of the CW end of travel limit input. It is affected by the active polarity, which is configured by the EndOfTravelLimitSetup parameter.
	'''
	CcwEndOfTravelLimitInput = 1 << 1,
	'''
	This represents the state of the CW end of travel limit input. It is affected by the active polarity, which is configured by the EndOfTravelLimitSetup parameter.
	'''
	HomeLimitInput = 1 << 2,
	'''
	This represents the state of the home limit input. It is affected by the active polarity, which is configured by the EndOfTravelLimitSetup parameter.
	'''
	MarkerInput = 1 << 3,
	'''
	This represents the state of the marker input.
	'''
	SineEncoderError = 1 << 4,
	'''
	An error condition is present on the Sine encoder input of the feedback device.
	'''
	CosineEncoderError = 1 << 5,
	'''
	An error condition is present on the Cosine encoder input of the feedback device.
	'''
	MarkerLatch = 1 << 6,
	'''
	The position of the marker is latched.
	'''
	EncoderClipping = 1 << 7,
	'''
	The on-board encoder multiplier detected that the input signals may be exceeding the maximum input range, which results in clipping of the encoder signals.
	'''
	HallAInput = 1 << 8,
	'''
	This represents the state of the Hall A input.
	'''
	HallBInput = 1 << 9,
	'''
	This represents the state of the Hall B input.
	'''
	HallCInput = 1 << 10,
	'''
	This represents the state of the Hall C input.
	'''
	RawCwEndOfTravelLimitInput = 1 << 11,
	'''
	This represents the state of the CW end of travel limit input at the primary feedback connector. It is not affected by the active polarity.
	'''
	RawCcwEndOfTravelLimitInput = 1 << 12,
	'''
	This represents the state of the CW end of travel limit input at the primary feedback connector. It is not affected by the active polarity.
	'''
	RawHomeLimitInput = 1 << 13,
	'''
	This represents the state of the home limit input at the primary feedback connector. It is not affected by the active polarity.
	'''
	MxQuadratureWarning = 1 << 14,
	'''
	The on-board encoder multiplier detected that the quadrature generation logic exceeded the maximum rate.
	'''
	MxQuadratureError = 1 << 15,
	'''
	The on-board encoder multiplier detected that overflow occurred in the quadrature generation logic.
	'''
	DigitalCosineInput0 = 1 << 16,
	'''
	This represents the state of the square wave cosine input or the digital interpretation of the sine wave cosine input from the feedback device.
	'''
	DigitalSineInput0 = 1 << 17,
	'''
	This represents the state of the square wave sine input or the digital interpretation of the sine wave sine input from the feedback device.
	'''
	DigitalCosineInput1 = 1 << 18,
	'''
	This represents the state of the square wave cosine input or the digital interpretation of the sine wave cosine input from the second feedback device.
	'''
	DigitalSineInput1 = 1 << 19,
	'''
	This represents the state of the square wave sine input or the digital interpretation of the sine wave sine input from the second feedback device.
	'''
	CwEotLimit = 1 << 0,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CwEndOfTravelLimitInput. Use CwEndOfTravelLimitInput instead of this enum value.
	'''
	CcwEotLimit = 1 << 1,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to CcwEndOfTravelLimitInput. Use CcwEndOfTravelLimitInput instead of this enum value.
	'''
	HomeLimit = 1 << 2,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to HomeLimitInput. Use HomeLimitInput instead of this enum value.
	'''
	RawCwEotLimit = 1 << 11,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to RawCwEndOfTravelLimitInput. Use RawCwEndOfTravelLimitInput instead of this enum value.
	'''
	RawCcwEotLimit = 1 << 12,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to RawCcwEndOfTravelLimitInput. Use RawCcwEndOfTravelLimitInput instead of this enum value.
	'''
	RawHomeLimit = 1 << 13,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to RawHomeLimitInput. Use RawHomeLimitInput instead of this enum value.
	'''
	DigitalCosineInput = 1 << 16,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to DigitalCosineInput0. Use DigitalCosineInput0 instead of this enum value.
	'''
	DigitalSineInput = 1 << 17,
	'''
	This enum value is deprecated and will be removed in the next major version of Automation1 software. This enum value has been renamed to DigitalSineInput0. Use DigitalSineInput0 instead of this enum value.
	'''

class AuxiliaryFeedbackStatus(CEnum):
	'''
	Represents the auxiliary feedback connector status bits
	'''
	_init_ = 'value __doc__',
	MarkerInput = 1 << 0,
	'''
	This represents the state of the marker input.
	'''
	SineEncoderError = 1 << 1,
	'''
	An error condition is present on the Sine encoder input of the feedback device.
	'''
	CosineEncoderError = 1 << 2,
	'''
	An error condition is present on the Cosine encoder input of the feedback device.
	'''
	MarkerLatch = 1 << 3,
	'''
	The position of the marker is latched.
	'''
	EncoderClipping = 1 << 4,
	'''
	The on-board encoder multiplier detected that the input signals may be exceeding the maximum input range, which results in clipping of the encoder signals.
	'''
	MxQuadratureWarning = 1 << 5,
	'''
	The on-board encoder multiplier detected that the maximum quadrature generation rate has been exceeded.
	'''
	MxQuadratureError = 1 << 6,
	'''
	The on-board encoder multiplier detected that the quadrature generation logic has experienced overflow.
	'''
	DigitalCosineInput = 1 << 7,
	'''
	This represents the state of the square wave cosine input or the digital interpretation of the sine wave cosine input from the feedback device.
	'''
	DigitalSineInput = 1 << 8,
	'''
	This represents the state of the square wave sine input or the digital interpretation of the sine wave sine input from the feedback device.
	'''

class AmplifierStatus(CEnum):
	'''
	Represents the amplifier status bits
	'''
	_init_ = 'value __doc__',
	Active = 1 << 0,
	'''
	The amplifier is active and outputting current to the attached motor.
	'''
	NoMotorSupply = 1 << 2,
	'''
	The amplifier detected that no motor supply voltage is present.
	'''
	CurrentClamp = 1 << 3,
	'''
	The amplifier output is being clamped because the current command is more than the value of the MaxCurrentClamp parameter.
	'''
	PowerLimitingA = 1 << 4,
	'''
	The amplifier power limiting on phase A has been active for an extended period. This causes an amplifier fault.
	'''
	PowerLimitingB = 1 << 5,
	'''
	The amplifier power limiting on phase B has been active for an extended period. This causes an amplifier fault.
	'''
	PowerLimitingC = 1 << 6,
	'''
	The amplifier power limiting on phase C has been active for an extended period. This causes an amplifier fault.
	'''
	PowerLimitingAUnfiltered = 1 << 7,
	'''
	The amplifier output on phase A is being limited to prevent damage to the hardware.
	'''
	PowerLimitingBUnfiltered = 1 << 8,
	'''
	The amplifier output on phase B is being limited to prevent damage to the hardware.
	'''
	PowerLimitingCUnfiltered = 1 << 9,
	'''
	The amplifier output on phase C is being limited to prevent damage to the hardware.
	'''
	BusOverVoltage = 1 << 10,
	'''
	The amplifier bus voltage is more than the maximum rated value.
	'''
	VoltageClamped = 1 << 11,
	'''
	The amplifier output on one or more phases is being clamped to the minimum or maximum voltage.
	'''
	ShuntOn = 1 << 12,
	'''
	The amplifier shunt circuit is active to keep the internal bus voltage within safe levels.
	'''

class SsiStatus(CEnum):
	'''
	Represents the SSI status for a feedback input.
	'''
	_init_ = 'value __doc__',
	TimeoutError = 1 << 0,
	'''
	The encoder did not respond in the necessary time interval.
	'''
	ParityError = 1 << 1,
	'''
	The parity calculated by the drive does not agree with the parity bit sent by the encoder.
	'''

class HyperWireExternalSynchronizationSignal(CEnum):
	'''
	Specifies the external signal with which to externally synchronize HyperWire.
	'''
	_init_ = 'value __doc__',
	None_ = 0,
	'''
	External synchronization is disabled.
	'''
	EthercatSync0 = 1,
	'''
	External synchronization is enabled with the EtherCAT SYNC0 signal.
	'''

class PsoWaveformExternalSyncDelayMode(CEnum):
	'''
	Represents the delay mode for the PSO waveform module when you use the external synchronization signal.
	'''
	_init_ = 'value __doc__',
	AfterExternalSync = 0,
	'''
	Applies the fixed delay after waiting for the rising edge of the external synchronization signal.
	'''
	BeforeExternalSync = 1,
	'''
	Applies the fixed delay after a PSO event occurs but before waiting for the rising edge of the external synchronization signal.
	'''

class DriveEncoderChannel(CEnum):
	'''
	Represents drive encoder channels that contain a hardware counter you can set.
	'''
	_init_ = 'value __doc__',
	AuxiliaryEncoder = 0,
	'''
	Auxiliary channel.
	'''
	SyncPortA = 1,
	'''
	Sync Port A channel.
	'''
	SyncPortB = 2,
	'''
	Sync Port B channel.
	'''
	HighSpeedOutputs = 3,
	'''
	High Speed Output channel.
	'''

