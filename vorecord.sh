#!/bin/bash

SOUND=0
FULLSCREEN=0
METHOD=""
RATE=30
VAAPI=0
OMX=0
DIR="$HOME"

export VAAPI_DISABLE_INTERLACE=1 #will duplicate and squish images otherwise

while getopts ":h?s?f?d:m:r:o:" opt; do
  case $opt in
    s)
      echo "Recording sound"
      SOUND=1
      SOUNDDEV=$(pacmd list | sed -n "s/.*<\(.*\\.monitor\)>/\\1/p" | head -1)
      ;;
    f)
      echo "Recording fullscreen"
      FULLSCREEN=1
      SOURCE="display-name=:0 use-damage=0 startx=0 starty=0 endx=1919 endy=1079"
      #SOURCE="display-name=:0 use-damage=0 startx=0 starty=0 endx=2159 endy=1199"
      ;;
    m)
      if [ "$OPTARG"x == "vaapix" ]
      then
        echo "Using vaapi encoding"
        VAAPI=1
      elif [ "$OPTARG"x == "omxx" ]
      then
        echo "Using omx encoding"
        OMX=1
      else
        echo "Unsupported encoding method: $OPTARG"
        exit 1
      fi
      ;;
    r)
      echo "Recording $OPTARG FPS"
      RATE=$OPTARG
      ;;
    o)
      echo "Parsed filename: $OPTARG"
      FILENAME=$OPTARG
      ;;
    d)
      echo "Recording to directory $OPTARG"
      DIR=$OPTARG
      ;;
    h)
      echo "Usage:"
      echo "$0 [-s] [-f] [-d directory|-o filename] [-r framerate] -m (vaapi|omx)"
      echo "-s: Record Pulseaudio sound from monitor $(pacmd list | sed -n "s/.*<\(.*\\.monitor\)>/\\1/p" | head -1)"
      echo "-f: Fullscreen. Window picker is used when omitted"
      echo "-r: Framerate in fps. Defaults to 30"
      echo "-d: Directory where a file 'rec_$(date +"%Y-%m-%d_%H%M%S").mkv' will be created"
      echo "-o: Filename will make the directory option useless. Supply full path or it will be created in the current working dir"
      exit 0
    ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $(($OPTIND - 1))

if [ "0" -eq "${FULLSCREEN}" ]
then
    echo "Choose a window to record"
    SOURCE="xid=$(xwininfo |grep 'Window id' | awk '{print $4;}') use-damage=0"

fi
echo "Recording..."

if [ $VAAPI -eq 1 ]
then
    #for constant bitrate: rate-control=cbr
    ENC="videoconvert ! video/x-raw,format=NV12,framerate=$RATE/1 ! multiqueue ! vaapih265enc rate-control=cqp bitrate=2000 ! video/x-h265 ! h265parse"
elif [ $OMX -eq 1 ]
then
    ENC="videoconvert ! video/x-raw,format=NV12,framerate=$RATE/1 ! multiqueue ! omxh264enc control-rate=2 target-bitrate=15000000 ! h264parse"
else
    echo "ERROR: Missing encoding method: -m vaapi or -m omx"
    exit 1
fi

if [ $SOUND -eq 1 ]
then
    SOUNDMUX=" pulsesrc device-name=$SOUNDDEV ! audio/x-raw,channels=2 ! multiqueue ! opusenc frame-size=40 complexity=6 ! multiqueue ! muxer. muxer."
else
    SOUNDMUX="."
fi

if [ -z $FILENAME ]
then
    FILENAME="$DIR/rec_$(date +"%Y-%m-%d_%H%M%S").mkv"
fi

echo "Recording to $FILENAME"

CMD="gst-launch-1.0 -e ximagesrc $SOURCE ! multiqueue ! video/x-raw,format=BGRx,framerate=$RATE/1 ! $ENC ! multiqueue ! matroskamux name=muxer$SOUNDMUX ! progressreport name=Rec_time ! filesink location=$FILENAME"
echo "$CMD"
eval "$CMD"
