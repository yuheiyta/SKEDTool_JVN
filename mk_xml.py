#!/usr/bin/python3
# AKIMOTO
# history as below
HISTORY = """
### History of this script
 2022-02-01
 2022-02-02 update1
 2022-02-04 update2
 2022-02-05 update3
 2022-02-14 update4
 2022-02-17 update5
 2022-02-18 update6
 2022-02-21 update7
 2022-02-28 update8
 2022-03-08 update9
 2022-05-10 update10
 2022-05-15 update11
 2022-05-25 update12
 2022-05-25 update13
 2023-02-07 update14

 Edit by M.AKIMOTO
### """

import re, os, sys, argparse, datetime

# help
if len(sys.argv) == 1 :
    program = os.path.basename(sys.argv[0])
    os.system("%s -h" % program)
    quit()

# original def func. made by AKIMOTO
error = "\033[32mError\033[0m"
sampling_frequency = 1024e+06
class original_function :
    
    def History() :
        if history == True :
            print(HISTORY)
            quit()

    # freq code (X, C) to 8192, 6600
    def freq_conv(f) :
        if   f in ["X", "+8192e+6", "8192"] :
            freq_out = "+8192e+6"
        elif f in ["C", "+6600e+6", "6600"] :
            freq_out = "+6600e+6"
        elif f == False :
            print("%s Please specify --frequency X/C." % error)
            quit()
        else :
            print("%s %s; Such a frequency code don't exist !!" % (error, f))
            quit()
        return freq_out
    
    # fft points check
    def fft_point_check(power_of_2) :
        fft = power_of_2
        while True :
            power_of_2 = power_of_2 / 2
            if power_of_2 == 1.0 :
                break
            elif power_of_2 < 1.0 :
                print("%s %.0f; FFT points isn't power of 2 !!" % (error, fft))
                quit()
            else:
                continue

    # overlapping
    def arguments_overlapping(A1, A2) : 
        if A1 != False and A2 != False :
            print("%s you can't specify %s & %s at the same time." % (error, A1, A2))
            quit()

    # file path
    def file_check(input_file) :
        F = input_file.split()
        for file in F :
            if file != "False" :
                file_check = os.path.isfile(file)
                if file_check == True :
                    print("File exist; %s" % file)
                else :
                    print("%s %s; Such a file don't exist !!" % (error, file))
                    quit()
            else :
                continue
            
    # convert DOY to month & day
    def cal_month_day(Year, DOY) :
        Year = int(Year) + 2000
        DOY  = int(DOY)
        doy2month_day = datetime.datetime(Year,1,1,0,0,0) + datetime.timedelta(days=DOY -1)
        month = doy2month_day.month
        day   = doy2month_day.day
        return Year, month, day

    # display schedule list of DRG-file
    def schedule_list(num, T, R, D) :
        list_line = ""
        if drg != False and list_ == True and num == 1:
            list_line = "###\n  Observation list\n###\n"
        if drg != False and list_ == True :
            list_line = " scan %2d > %s  %s  %s\n" % (num, T, R, D)
        return list_line
    
    def split_double(line, S) :
        split_out = line.split("<%s>" % S)[-1].split("</%s>" % S)[0]
        return split_out

    def re_findall_replace(replace_target, xml_line_string) :
        replace_find = re.findall("<%s>.*</%s>" % (replace_target, replace_target), xml_line_string)
        return replace_find
    
    def re_findall_result(change_before, change_after, element) :
        change_result = xml_line.replace("%s" % change_before, "<%s>%s</%s>" % (element, change_after, element))
        return change_result


# arguments
class MyHelpFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass

description = \
"""
### USAGE
    This script make two type XML-file of your observation from DRG-file.
    First, this script make xml-file of the only fringe-finder for 
    searching fringe of your observation data then this script make 
    xml-file of all your observation schedule by using xml-file of 
    fringe-finder.
###
### EXAMPLE
    If you make xml-file of fringe-finder, you should specify 
    arguments, --drg, --scan, --length & --frequency.
    >> $ %s --drg I21001.DRG --scan 10 --length 10 --frequency X

    If you make xml-file of all the observation schedule, you 
    should specify arguments, --xml & --sample-deay at least.
    >> %s --xml I21001_10_KL.xml --sample-delay 86
###
    Please read the last message, attentions of this program !!
    Thsnks (^^), This script is made by M.AKIMOTO on 2022/02/01. 
""" % (os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]))
epilog = \
"""
### ATTENTION
        You can not specify --drg and --xml at the same time. A new
    xml-file is made if you specify --drg, however the xml-file
    inputted by specifying --xml already inserts all the correlation 
    processing schedule. 
        In addition, you can not specify --log and --recstart at 
    the same time to. If you don't prepare octadisk-/vsrec-log files
    you can specify --recstart.
###
"""
parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=MyHelpFormatter)  

parser.add_argument("--drg"         , default=False     , type=str                                      , help="drg-file of the observing schedule")
parser.add_argument("--xml"         , default=False     , type=str                                      , help="xml-file outputted by this script ")
parser.add_argument("--log"         , default=False     , type=str                                      , help="octa-/vsrec-log file")
parser.add_argument("--delay"       , default="+1.6e-06", type=float                                    , help="delay. in case of YI, you don't have to specify this option.")
parser.add_argument("--rate"        , default="+0.0e-00", type=float                                    , help="rate. in case of YI, you don't must specify this option.")
parser.add_argument("--fft"         , default="1024"    , type=int                                      , help="fft points. the power of 2.")
parser.add_argument("--scan"        , default="0"       , type=int  , nargs="+"                         , help="scan number of fringe-finder")
parser.add_argument("--length"      , default="1"       , type=int                                      , help="the integration time of the target but smaller than its duration")
parser.add_argument("--frequency"   , default=False     , type=str  , choices=["X", "8192", "C", "6600"], help="which frequency do you carry out the observation by using ?.")
parser.add_argument("--output"      , default="1"       , type=int                                      , help="the output")
parser.add_argument("--label"       , default=False     , type=str                                      , help="the label of cor-files, ant1_ant2_recstarttime_label.cor")
parser.add_argument("--sample-delay", default="0"       , type=float, dest="SampleDelay"                , help="redidual delay of fringe search. unit is \"smaple\"")
parser.add_argument("--sample-rate" , default="0"       , type=float, dest="SampleRate"                 , help="redidual rate of fringe search. unit is \"Hz\". in case of YI, you don't must specify this program.")
parser.add_argument("--recorder"    , default="vsrec"   , type=str  , choices=["octadisk", "vsrec"]     , help="which recorder do you use ?")
parser.add_argument("--recstart"    , default=False     , type=str                                      , help="octa-/vsrec-recording start-time if you don't prepare their log-file.")
parser.add_argument("--type"        , default="2"       , type=int  , choices=[1, 2]                    , help="xml schedule type; 1 is that the start-time of the correlation processing is the observing time of each scan but 2 is the recording start-time.")
parser.add_argument("--list"        , action="store_true"                                               , help="display your observing schedule")
parser.add_argument("-y", "--yes"   , action="store_true"                                               , help="skip the answer of the inputted parameter confirmations")
parser.add_argument("--history"     , action="store_true")

args = parser.parse_args() 
drg    = args.drg
xml    = args.xml
log    = args.log
delay  = args.delay
rate   = args.rate
fft    = args.fft
scan   = args.scan
length = args.length
freq   = args.frequency
output = args.output
label  = args.label
sample_delay = args.SampleDelay
sample_rate  = args.SampleRate
recorder = args.recorder
recstart = args.recstart
type_    = args.type
list_    = args.list
yes      = args.yes
history  = args.history

# arguments check
original_function.arguments_overlapping(drg, xml)
original_function.arguments_overlapping(log, recstart)

# file path check
original_function.file_check("%s %s %s" % (drg, xml, log))

# history of this script
original_function.History()

#######################
### main
#######################
if xml == False :

    # empty value & list
    i = 0
    source_line      = ""
    xml_process_line = ""
    obs_scan_list    = ""

    # convert frequency (X, C) to 8192, 6600
    freq = original_function.freq_conv(freq)

    # FFT point check
    original_function.fft_point_check(fft)

    # REQRECSTART from octa-/vsrec-log or valuable "recstart"
    if type_ == 2 :
        if recstart == False and log != False :
            log_open = open(log, "r").readlines()
            for line in log_open :
                REQRECSTART_line = "$REQRECSTART" in line
                if REQRECSTART_line == True :
                    octa_vsrec_log_REQRECTIME = line.split()[-1]
            try :
                if not octa_vsrec_log_REQRECTIME :
                    pass
            except NameError :
                print("\"$REQRECSTART\" isn't inserted in %s." % log)
                print("Please check %s" % log)
                quit()
        elif recstart != False and log == False :
                octa_vsrec_log_REQRECTIME = recstart
        elif log == False or recstart == False :
            print("%s You must specify --log or --recstart if you specify --type=2" % error)
            quit()
        else :
            print("%s Please arguments which you input in this script." % error)
            print(epilog)
            quit()

        xml_process_line += "<!-- recstart-time of OCTADISK/VSREC from octa-/vsrec-log file; %s -->\n\n" % octa_vsrec_log_REQRECTIME

        # reference time in xml-file (its year, month & day)
        rectime_start = octa_vsrec_log_REQRECTIME
        rectime_Year, rectime_month, rectime_day = original_function.cal_month_day(rectime_start[2:4], rectime_start[4:7])

    # open DRG-file
    drg_open = open(drg, "r").readlines()

    for drg_line in drg_open :
        
        sked_line1 = "2000.0" in drg_line
        sked_line2 = "PREOB"  in drg_line
        
        if sked_line1 == True : # target coordinate
            source = drg_line.split()
            source_line += "<source name= \'%s\'><ra>%sh%sm%s</ra><dec>%sd%s\'%s</dec></source>\n" \
                            % (source[0], source[2], source[3], source[4], source[5], source[6], source[7])
        elif sked_line2 == True : # target obsevation schedule
            
            i += 1
            target   = drg_line.split()[0] # the info. of DRG-file
            rectime  = drg_line.split()[4]
            duration = drg_line.split()[5]
            baseline = drg_line.split()[9].replace("-", "")
            
            Year, month, day = original_function.cal_month_day(rectime[0:2], rectime[2:5]) # convert DOY to month & day
            hhmmss = "%s:%s:%s" % (rectime[5:7], rectime[7:9], rectime[9:11])
            
            # individual xml-file
            if not scan :
                print("%s Please specify --scan." % error)
                quit()
            elif i == scan[0] :
                rectime_scan = rectime
                label = "%.0f" % i
                file_label = "%.0f" % i
                            
            # Observation schedule list
            obs_scan_list += original_function.schedule_list(i, target.ljust(8), rectime, duration.rjust(4))
            
            # target length < --length
            if i == scan[0] and int(duration) < length :
                print("%s integration time (%.0f) is longer than duration (%s) of %s." % (error, length, duration, target))
                quit()
            
            if type_ == 1 :
                each_epoch_start = "20%s" % rectime
                skip_time        = "0"
                if i == scan[0] :
                    duration_scan = "%s" % length
                duration_time = duration
            elif type_ == 2 :
                # calculate skip time
                differential_time = datetime.datetime(year=Year, month=month, day=day, hour=int(rectime[5:7]), minute=int(rectime[7:9]), second=int(rectime[9:11])) \
                                            - datetime.datetime(year=rectime_Year, month=rectime_month, day=rectime_day, hour=int(rectime_start[7:9]), minute=int(rectime_start[9:11]), second=int(rectime_start[11:13]))
                
                skip_time     = "%.0f" % differential_time.total_seconds()
                duration_time = "%.0f" % (int(skip_time) + int(duration))
                duration_scan = "%.0f" % (int(skip_time) + length)
                
                each_epoch_start = rectime_start

            if i == scan[0] :
                xml_process_line += "<process><epoch>20%s/%s  %s:%s:%s</epoch><skip>%s</skip><length>%s</length><object>%s</object><stations>%s</stations></process> <!-- scan %2d  obs-date: 20%s-%02d-%02d %s --> <!-- fringe finder -->\n" \
                                    % (each_epoch_start[2:4], each_epoch_start[4:7], each_epoch_start[7:9], each_epoch_start[9:11], each_epoch_start[11:13], skip_time.rjust(5), duration_scan.rjust(4), target.rjust(8), baseline, i, rectime[0:2], month, day, hhmmss)
                                    
            xml_process_line += "<!-- ### <process><epoch>20%s/%s  %s:%s:%s</epoch><skip>%s</skip><length>%s</length><object>%s</object><stations>%s</stations></process> ### --> <!-- scan %2d  obs-date: 20%s-%02d-%02d %s -->\n" \
                                % (each_epoch_start[2:4], each_epoch_start[4:7], each_epoch_start[7:9], each_epoch_start[9:11], each_epoch_start[11:13], skip_time.rjust(5), duration_time.rjust(5), target.rjust(8), baseline, i, rectime[0:2], month, day, hhmmss)

    if list_ == True :
        print(obs_scan_list)
        quit()
    if scan == 0 :
        print("%s You need to select scan number of fringe-finder to calculate \"delay\" !!" % error)
        quit()

    # parameter check
    print("###")
    print(" recorder  : %s" % recorder)
    print(" octa-log  : %s" % log     )
    print(" DRG-file  : %s" % drg     )
    print(" Scan      : %s" % scan[0] )
    print(" FFT       : %s" % fft     )
    print(" Delay     : %s" % delay   )
    print(" Rate      : %s" % rate    )
    print(" Length    : %s" % length  )
    print(" Baseline  : %s" % baseline)
    print(" Frequency : %s" % freq    )
    print("###")
    # yes or no
    if yes != True:
        while True:
            answer = input("Are the above paramters correct ? [y/n] : ")
            if answer == "y":
                break
            elif answer == "n" :
                print("### Please start over !")
                quit()
            else :
                print(">> The answer is \"y\" or \"n\"")
elif xml != False : # make xml-file of all scan

    xml_all      = ""
    process_line = 0
    file_label   = "scan"
    
    xml_open = open(xml, "r").readlines()

    # edit individual xml-file
    for xml_line in xml_open :
        
        fft_line      = "<fft>"       in xml_line
        delay_line    = "<delay>"     in xml_line
        rate_line     = "<rate>"      in xml_line
        skd_line      = "<!-- ###"    in xml_line
        baseline_line = "<stations>"  in xml_line
        xml_process   = "<process>"   in xml_line
        xml_footer    = "</schedule>" in xml_line
        
        if skd_line == True : # xml-file all schedule <process>*</process>
            process_line += 1
            commentout_left  = re.findall("<!-- ###", xml_line)
            commentout_right = re.findall("### -->" , xml_line)
            xml_line = xml_line.replace("%s " % commentout_left[0] , "")
            xml_line = xml_line.replace("%s"  % commentout_right[0], "")
            if not scan in [0, "all"] :
                for s in scan :
                    if s == process_line :
                        file_label += "-%.0f" % s
                        xml_all += xml_line
                    else :
                        continue
            elif scan in [0, "all"] :
                scan = "all"
                xml_all += xml_line
        elif baseline_line == True : # baseline
            baseline = original_function.split_double(xml_line, "stations")
        elif fft_line == True :
            F1, F2, L = False, False, False
            for i in range(4) :
                fft_change    = original_function.re_findall_replace("fft", xml_line)
                label_change  = original_function.re_findall_replace("label", xml_line)
                freq_change   = original_function.re_findall_replace("frequency", xml_line)
                output_change = original_function.re_findall_replace("output", xml_line)
                if F1 != True and fft != 1024 : # FFT
                    F1 = True; original_function.fft_point_check(fft)
                    xml_line = original_function.re_findall_result(fft_change[0], fft, "fft")
                elif L != True and label != False : # label
                    L = True
                    if not scan in [0, "all"] :
                        xml_line = original_function.re_findall_result(label_change[0], label, "label")
                    elif scan in [0, "all"] :
                        file_label = label
                        xml_line = original_function.re_findall_result(label_change[0], label, "label")
                elif L != True and label == False : # label for spcifying --scan
                    L = True
                    if not scan in [0, "all"] :
                        label = "scan"
                        xml_line = original_function.re_findall_result(label_change[0], label, "label")
                    elif scan in [0, "all"] :
                        label = "all"; file_label = "all"
                        xml_line = original_function.re_findall_result(label_change[0], label, "label")
                elif F2 != True and freq != False : # frequency
                    F2 = True; freq = original_function.freq_conv(freq)
                    xml_line      = original_function.re_findall_result(freq_change[0], freq, "frequency")
                    freq_original = float(freq)
                elif F2 != True and freq == False : # frequency
                    F2 = True; freq = original_function.split_double(freq_change[0], "frequency")
                    freq_original = float(freq)
                elif output != "1" : # output
                    xml_line = original_function.re_findall_result(output_change[0], output, "output")
                xml_line = xml_line
            xml_all += xml_line
        elif delay_line == True: # <delay>*</delay> & <rate>*</rate>
            D, R = False, False
            for j in range(2) :
                # delay
                delay_change = original_function.re_findall_replace("delay", xml_line)
                delay_origin = original_function.split_double(delay_change[0], "delay")
                delay, sample_delay, delay_origin = float(delay), float(sample_delay), float(delay_origin)
                if  D != True and delay == delay_origin :
                    D = True; delay_total = delay + sample_delay / sampling_frequency
                elif D != True and delay != +1.6e-06 :
                    D = True; delay_total = delay + sample_delay / sampling_frequency
                elif D != True and delay_origin != +1.6e-06 :
                    D = True; delay_total = delay_origin + sample_delay / sampling_frequency
                xml_line = original_function.re_findall_result(delay_change[0], "%e" % delay_total, "delay")

                # rate
                rate_change = original_function.re_findall_replace("rate", xml_line)
                rate_origin = original_function.split_double(rate_change[0], "rate")
                rate, sample_rate, rate_origin = float(rate), float(sample_rate), float(rate_origin)
                if R != True and rate == rate_origin :
                    R = True; rate_total = rate + sample_rate / freq_original
                elif R != True and rate != 0.0 :
                    R = True; rate_total = rate + sample_rate / freq_original
                elif R != True and rate_origin != 0.0 :
                    R = True; rate_total = rate_origin + sample_rate / freq_original
                xml_line = original_function.re_findall_result(rate_change[0] , "%e" % rate_total , "rate")
            xml_all += xml_line
        elif xml_footer == True: # </schedule>
            xml_all += xml_line
        else :
            xml_all += xml_line

    # parameter check
    print("###")
    print(" xml-file    : %s" % xml)
    print(" fft         : %s" % fft)
    print(" total delay : %s" % delay_total)
    print(" total rate  : %s" % rate_total)
    print(" frequency   : %+3.3e" % freq_original)
    print(" stations    : %s" % baseline)
    print(" scan        : %s" % scan)
    print(" label       : %s" % label)
    print(" output      : %s" % output)
    print("###")

    # make xml-file of all scan Ver.
    xml_name = "%s_%s_%s.xml" % (xml.split("_")[0], file_label, baseline)
    xml_save = open(xml_name, "w")
    xml_save.write(xml_all)
    xml_save.close()
    
    print("make file > %s" % xml_name)
    quit()

# xml-file header, clock, stream
xml_header = \
"""<?xml version='1.0' encoding='UTF-8' ?>
<schedule>"""

xml_ADS = \
"""
<terminal name='ADS1000'><speed>1024000000</speed><channel> 1</channel><bit>2</bit><level>-1.5,+0.5,-0.5,+1.5</level></terminal>
<terminal name='ADS3000'><speed>1024000000</speed><channel>1</channel><bit>2</bit><level>-1.5,-0.5,+0.5,+1.5</level></terminal>  
<terminal name='ADS3000_OCT'><speed>1024000000</speed><channel>1</channel><bit>2</bit><level>-1.5,+0.5,-0.5,+1.5</level></terminal>"""
xml_station = \
"""
<station key='O'><name>KASHIM34</name><pos-x>-3997650.05799</pos-x><pos-y>+3276690.07124</pos-y><pos-z>+3724278.43114</pos-z><terminal>ADS3000</terminal></station> 
<station key='H'><name>HITACH32</name><pos-x>-3961788.9740</pos-x><pos-y>+3243597.4920</pos-y><pos-z>+3790597.6920</pos-z><terminal>ADS3000_OCT</terminal></station> 
<station key='T'><name>TAKAHA32</name><pos-x>-3961881.8250</pos-x><pos-y>+3243372.4800</pos-y><pos-z>+3790687.4490</pos-z><terminal>ADS3000_OCT</terminal></station>"""
if recorder == "octadisk" :
    xml_station += \
"""
<station key='%s'><name>YAMAGU32</name><pos-x>-3502544.587</pos-x><pos-y>+3950966.235</pos-y><pos-z>+3566381.192</pos-z><terminal>ADS3000_OCT</terminal></station>
<station key='%s'><name>YAMAGU34</name><pos-x>-3502567.576</pos-x><pos-y>+3950885.734</pos-y><pos-z>+3566449.115</pos-z><terminal>ADS3000_OCT</terminal></station>
""" % (baseline[0:1], baseline[1:2])
elif recorder == "vsrec" :
    xml_station += \
"""
<station key='%s'><name>YAMAGU32</name><pos-x>-3502544.587</pos-x><pos-y>+3950966.235</pos-y><pos-z>+3566381.192</pos-z><terminal>ADS3000</terminal></station>
<station key='%s'><name>YAMAGU34</name><pos-x>-3502567.576</pos-x><pos-y>+3950885.734</pos-y><pos-z>+3566449.115</pos-z><terminal>ADS3000</terminal></station>

<!-- VSREC bit shuffle -->
<shuffle key='%s'>24,25,26,27,28,29,30,31,16,17,18,19,20,21,22,23,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7</shuffle>
<shuffle key='%s'>24,25,26,27,28,29,30,31,16,17,18,19,20,21,22,23,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7</shuffle>
""" % (baseline[0:1], baseline[1:2], baseline[0:1], baseline[1:2])

xml_stream = \
"""<stream>
<label>%s</label><frequency>%s</frequency><channel>1</channel><fft>%s</fft><output>%s</output>
<special key='%s'><sideband>LSB</sideband></special>
<special key='%s'><sideband>LSB</sideband></special>
</stream>
""" % (label, freq, fft, output, baseline[0:1], baseline[1:2]) # L = label, F1 = frequency, F2 = FFT, O = output

xml_clock = "<clock key='%s'><epoch>20%s/%s  %s:%s:%s</epoch><delay>%s</delay><rate>%s</rate></clock> <!-- scan %.0f -->\n" % (baseline[1:2], rectime_scan[0:2], rectime_scan[2:5], rectime_scan[5:7], rectime_scan[7:9], rectime_scan[9:11], delay, rate, scan[0])

# make xml-file
xml_base = os.path.splitext(os.path.basename(drg))[0]
xml_name = "%s_%.0f_%s.xml" % (xml_base, scan[0], baseline)
xml_save = open(xml_name, "w")
xml_save.write("%s\n" % xml_header)
xml_save.write("%s\n" % xml_ADS)
xml_save.write("%s\n" % xml_station)
xml_save.write("%s\n" % source_line)
xml_save.write("%s\n" % xml_stream)
xml_save.write("%s\n" % xml_clock)
xml_save.write("%s\n" % xml_process_line)
xml_save.write("</schedule>")
xml_save.close()

print("make file > %s" % xml_name)
