#-*- coding: gbk -*-

import LogMod

if __name__ == '__main__' :
    l = LogMod.LogMod()
    l.Warning("Test a warning")
    l.Fatal("Test a fatal case")
    l.Notice("Test a Notice")