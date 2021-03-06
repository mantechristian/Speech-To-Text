import os
import numpy as np
import configparser
import sounddevice as sd
import constants as const
from scipy.io.wavfile import write


class RecordAudio:
    def __init__(self):
        self.configParser = configparser.ConfigParser()
        self.configParser.read(const.CONFIG_FILE_NAME)
        self.samplingFreq = self.configParser.getint(const.CFG_AUDIO_REC, const.CFG_REC_FREQ)
        self.recordingDuration = self.configParser.getint(const.CFG_AUDIO_REC, const.CFG_REC_DURATION)
        self.audio_path = self.configParser.get(const.CFG_AUDIO_DIR, const.CFG_AUDIO_PATH)
        self.audio_file_name = self.configParser.get(const.CFG_AUDIO_DIR, const.CFG_AUDIO_FILE_NAME)
        self.audio_file_path = os.path.join(self.audio_path, self.audio_file_name)

    def startRecording(self):
        duration = self.recordingDuration
        myrecording = sd.rec(int(duration * self.samplingFreq), samplerate=self.samplingFreq, channels=2)
        sd.wait()
        myrecording = (np.iinfo(np.int32).max * (myrecording/np.abs(myrecording).max())).astype(np.int32)
        return myrecording
    
    # def callback(self, indata, outdata, frames, time, status):
    #     print("callback")
    #     if status:
    #         print(status)
    #     outdata[:] = indata
    #     y = (np.iinfo(np.int32).max * (outdata/np.abs(outdata).max())).astype(np.int32)
    #     audio_file_path = os.path.join(self.audio_path, self.audio_file_name)
    #     write(audio_file_path, self.samplingFreq, y)
    
    def start(self):
        print("Start Recording ...")
        try:
            myrecording = self.startRecording()
            sd.play(myrecording)
            write(self.audio_file_path, self.samplingFreq, myrecording)
            # with sd.Stream(channels=2, callback=self.callback):
            #     sd.sleep(int(self.recordingDuration * 1000))
        except Exception as e:
            print (e)
            print("An error ocurred while recording the audio.")

if __name__ == "__main__":
    recorder = RecordAudio()
    recorder.start()
