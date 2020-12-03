import os


class stream:
    def __init__(self, filename):
        self.name = filename
        self.outputs = ["720", "480", "240", "120"]
        self.files = ['output_720.mp4', 'output_480.mp4', 'output_240.mp4', 'output_120.mp4']

    def resolution_change(self):
        os.system("ffmpeg -ss 00:07:56 -i %s -map 0:0 -c:v copy -map 0:1 -map 0:2 -c:a copy -t 10 output.mp4"
                  % self.name)
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=1280:720 -map 0:1 -map 0:2 -c:a copy output_720.mp4')
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=854:480 -map 0:1 -map 0:2 -c:a copy output_480.mp4')
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=360:240 -map 0:1 -map 0:2 -c:a copy output_240.mp4')
        os.system('ffmpeg -i output.mp4 -map 0:0 -vf scale=160:120 -map 0:1 -map 0:2 -c:a copy output_120.mp4')

    def codec_changer(self):
        for i in range(len(self.files)):
            os.system("ffmpeg -i %s -c:v libvpx -c:a libvorbis output_%s_vp8.webm"
                      % (self.files[i], self.outputs[i]))
            os.system("ffmpeg -i %s -c:v libvpx-vp9 -c:a libvorbis output_%s_vp9.webm"
                      % (self.files[i], self.outputs[i]))
            os.system("ffmpeg -i %s -c:v libx265 -c:a ac3 output_%s_h265.mp4"
                      % (self.files[i], self.outputs[i]))
            os.system("ffmpeg -i %s -c:v libaom-av1 -c:a libvorbis output_%s_AV1.mkv"
                      % (self.files[i], self.outputs[i]))

    def codec_collage(self):
        os.system('ffmpeg -i output_720_vp8.webm -i output_720_vp9.webm -i output_720_h265.mp4 -i output_720_AV1.mkv '
                  '-filter_complex "nullsrc=size=1280x720 [base]; [0:v] setpts=PTS-STARTPTS, scale=640x360 ['
                  'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=640x360 [upperright]; [2:v] setpts=PTS-STARTPTS, '
                  'scale=640x360 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=640x360 [lowerright]; [base]['
                  'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=640 [tmp2]; [tmp2]['
                  'lowerleft] overlay=shortest=1:y=360 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=640:y=360" '
                  '-c:v libvpx-vp9 collage_720.webm')
        os.system('ffmpeg -i output_480_vp8.webm -i output_480_vp9.webm -i output_480_h265.mp4 -i output_480_AV1.mkv '
                  '-filter_complex "nullsrc=size=854x480 [base]; [0:v] setpts=PTS-STARTPTS, scale=427x240 ['
                  'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=427x240 [upperright]; [2:v] setpts=PTS-STARTPTS, '
                  'scale=427x240 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=427x240 [lowerright]; [base]['
                  'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=427 [tmp2]; [tmp2]['
                  'lowerleft] overlay=shortest=1:y=240 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=427:y=240" '
                  '-c:v libvpx-vp9 collage_480.webm')
        os.system('ffmpeg -i output_240_vp8.webm -i output_240_vp9.webm -i output_240_h265.mp4 -i output_240_AV1.mkv '
                  '-filter_complex "nullsrc=size=360x240 [base]; [0:v] setpts=PTS-STARTPTS, scale=180x120 ['
                  'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=180x120 [upperright]; [2:v] setpts=PTS-STARTPTS, '
                  'scale=180x120 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=180x120 [lowerright]; [base]['
                  'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=180 [tmp2]; [tmp2]['
                  'lowerleft] overlay=shortest=1:y=120 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=180:y=120" '
                  '-c:v libvpx-vp9 collage_240.webm')
        os.system('ffmpeg -i output_120_vp8.webm -i output_120_vp9.webm -i output_120_h265.mp4 -i output_120_AV1.mkv '
                  '-filter_complex "nullsrc=size=160x120 [base]; [0:v] setpts=PTS-STARTPTS, scale=80x60 ['
                  'upperleft]; [1:v] setpts=PTS-STARTPTS, scale=80x60 [upperright]; [2:v] setpts=PTS-STARTPTS, '
                  'scale=80x60 [lowerleft]; [3:v] setpts=PTS-STARTPTS, scale=80x60 [lowerright]; [base]['
                  'upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] overlay=shortest=1:x=80 [tmp2]; [tmp2]['
                  'lowerleft] overlay=shortest=1:y=60 [tmp3]; [tmp3][lowerright] overlay=shortest=1:x=80:y=60" '
                  '-c:v libvpx-vp9 collage_120.webm')


ex1 = stream("input.mp4")
ex1.codec_collage()
