from ChromaCqt import ChromaCqt

#実装サンプル
cc1=ChromaCqt()
cc1.load_music('file.wav')
#cc1.cut(cc1.loaded_data,7,56)
#cc1.lr_separate(cc1.cut_data)
cc1.lr_separate(cc1.loaded_data)
cc1.hpss_execute(cc1.lr_separated_data,'right')
cc1.chromacqt_execute(cc1.hpss_data['harmonic'])
print(cc1.chrcqt_data)
cc1.disp_chrcqt(cc1.chrcqt_data)
cc1.export_csv()
cc1.create_io_array()