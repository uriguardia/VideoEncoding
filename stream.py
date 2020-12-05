import os
import subprocess


# Here I have created the class stream
class stream:
    # We create the constructor method that takes as input the input file as well as an ip address.
    def __init__(self, filename, ip):
        self.name = filename
        self.ip = ip
        # We create the variables outputs and files that will be needed next.
        self.outputs = ["720", "480", "240", "120"]
        self.files = ['output_720.mp4', 'output_480.mp4', 'output_240.mp4', 'output_120.mp4']

    def resolution_changer(self):
        # This method takes the input file and creates 4 with different resolutions(720p, 480p, 240p, 120p). I have
        # decided to use only a segment of ten seconds of the video because of performance, especially in the case of
        # the 720p video.
        os.system("ffmpeg -ss 00:07:56 -i %s -map 0:0 -c:v copy -map 0:1 -map 0:2 -c:a copy -t 10 output.mp4"
                  % self.name)
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=1280:720 -map 0:1 -map 0:2 -c:a copy output_720.mp4')
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=854:480 -map 0:1 -map 0:2 -c:a copy output_480.mp4')
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=360:240 -map 0:1 -map 0:2 -c:a copy output_240.mp4')
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=160:120 -map 0:1 -map 0:2 -c:a copy output_120.mp4')

    def codec_changer(self):
        # Here for each video of the 4 created before we perform video codec change in the following order( VP8, VP9,
        # H265 and AV1). In my case i did not only change the video coder but the whole container because I want it to
        # try. In the case of the AV1 the encoding time is very very very very very very slow and that is the reason I
        # decided to cut ten seconds of the video earlier. Also for the audio encoder I checked the ffmpeg page in order
        # to see which ones fit the best for each package. (https://trac.ffmpeg.org/wiki/Encode/HighQualityAudio)
        for i in range(len(self.files)):
            os.system("ffmpeg -i %s -c:v libvpx -c:a libvorbis output_%s_vp8.webm"
                      % (self.files[i], self.outputs[i]))
            os.system("ffmpeg -i %s -c:v libvpx-vp9 -c:a libvorbis output_%s_vp9.webm"
                      % (self.files[i], self.outputs[i]))
            os.system("ffmpeg -i %s -c:v libx265 -c:a ac3 output_%s_h265.mp4"
                      % (self.files[i], self.outputs[i]))
            os.system("ffmpeg -i %s -c:v libaom-av1 -c:a libvorbis output_%s_AV1.mkv"
                      % (self.files[i], self.outputs[i]))

    def vlc_stream(self):
        # In this method we want to stream the input file to the ip given in the constructor. With mpegts command of
        # the ffmpeg we can compute the streaming. Then in parallel the command to receive the stream to VLC must be
        # given as well. Since it is in parallel I will be using the subprocess library. So both commands are stored
        # in an array, and then iterated through to use Popen in order to execute them. Then from what I have seen it
        # is good practice to use the .wait() method, because a Popen object has a .wait() method exactly defined for
        # this: to wait for the completion of a given subprocess
        command = ["ffmpeg -re -i %s -map 0:0 -c:v copy -map 0:1 -map 0:2 -c:a copy -f mpegts udp://%s:1234"
                   % (self.name, self.ip), "vlc udp://@%s:1234" % self.ip]
        # Run commands in parallel
        processes = []

        for i in range(len(command)):
            process = subprocess.Popen(command[i], shell=True)
            processes.append(process)

        # Collect statuses
        output = [p.wait() for p in processes]


def codec_collage():
    # This a function by itself created in order to perform a collage of the quality of encoding for each scale. I tried
    # to output the video in a good quality video encoder in order not to bottleneck. In the upper left we have
    # VP8, then in the upper right VP9, in the lower left h265 and finally in the lower right AV1.

    # In the 720p scale we can observe, especially in the quality of the fur or the background, that AV1 is much
    # better than the rest. From VP9 to h265 I do not see much difference in my case and finally VP8 has the worst
    # quality.
    os.system('ffmpeg -i output_720_vp8.webm -i output_720_vp9.webm -i output_720_h265.mp4 -i output_720_AV1.mkv '
              '-filter_complex "nullsrc=size=1280x720 [base]; [0:v] setpts=PTS-STARTPTS, scale=640x360 ['
              'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=640x360 [upperright]; [2:v] setpts=PTS-STARTPTS, '
              'scale=640x360 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=640x360 [lowerright]; [base]['
              'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=640 [tmp2]; [tmp2]['
              'lowerleft] overlay=shortest=1:y=360 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=640:y=360" '
              '-c:v libvpx-vp9 collage_720.webm')
    # In the case of 480p is pretty much the same story.
    os.system('ffmpeg -i output_480_vp8.webm -i output_480_vp9.webm -i output_480_h265.mp4 -i output_480_AV1.mkv '
              '-filter_complex "nullsrc=size=854x480 [base]; [0:v] setpts=PTS-STARTPTS, scale=427x240 ['
              'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=427x240 [upperright]; [2:v] setpts=PTS-STARTPTS, '
              'scale=427x240 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=427x240 [lowerright]; [base]['
              'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=427 [tmp2]; [tmp2]['
              'lowerleft] overlay=shortest=1:y=240 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=427:y=240" '
              '-c:v libvpx-vp9 collage_480.webm')
    # 240p has so bad quality that is very difficult to differentiate between codecs.
    os.system('ffmpeg -i output_240_vp8.webm -i output_240_vp9.webm -i output_240_h265.mp4 -i output_240_AV1.mkv '
              '-filter_complex "nullsrc=size=360x240 [base]; [0:v] setpts=PTS-STARTPTS, scale=180x120 ['
              'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=180x120 [upperright]; [2:v] setpts=PTS-STARTPTS, '
              'scale=180x120 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=180x120 [lowerright]; [base]['
              'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=180 [tmp2]; [tmp2]['
              'lowerleft] overlay=shortest=1:y=120 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=180:y=120" '
              '-c:v libvpx-vp9 collage_240.webm')
    # In 120p it is same with 240p.
    os.system('ffmpeg -i output_120_vp8.webm -i output_120_vp9.webm -i output_120_h265.mp4 -i output_120_AV1.mkv '
              '-filter_complex "nullsrc=size=160x120 [base]; [0:v] setpts=PTS-STARTPTS, scale=80x60 ['
              'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=80x60 [upperright]; [2:v] setpts=PTS-STARTPTS, '
              'scale=80x60 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=80x60 [lowerright]; [base]['
              'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=80 [tmp2]; [tmp2]['
              'lowerleft] overlay=shortest=1:y=60 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=80:y=60" '
              '-c:v libvpx-vp9 collage_120.webm')


address = "192.168.1.39"
twitch = stream("input.mp4", address)
twitch.vlc_stream()
# codec_collage()
