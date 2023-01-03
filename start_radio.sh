adb connect 192.168.2.95
sleep 2
python /home/hendrik/Documents/General/control_tv.py Up
adb shell am start -a android.intent.action.VIEW -d "https://www.youtube.com/watch?v=NTEPBVmyqPY" com.google.android.youtube.tv
