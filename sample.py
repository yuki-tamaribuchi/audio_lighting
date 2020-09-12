from ChromaCqt import ChromaCqt

#実装サンプル
cc1=ChromaCqt()
cc1.load_music('file.wav')
cc1.lr_separate(cc1.normalized_data)
cc1.hpss_execute(cc1.lr_separated_data)
cc1.chromacqt_execute(cc1.hpss_data['left']['harmonic'])
print(cc1.chrcqt_data)
#cc1.disp_chrcqt(cc1.chrcqt_data)
#cc1.export_csv()
#cc1.create_io_array()
