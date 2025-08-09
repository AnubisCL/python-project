import win32gui
import win32process
from pymem import *

WindowHandle = win32gui.FindWindow("Window","植物大战僵尸杂交版v2,0,88")
ThreadId, ProcessId = win32process.GetWindowThreadProcessId(WindowHandle)

PROCESS_ALL_ACCESS = (0x000F0000|0x00100000|0xFFF)
ProcessHandle = pymem.process.open(ProcessId, True, PROCESS_ALL_ACCESS)