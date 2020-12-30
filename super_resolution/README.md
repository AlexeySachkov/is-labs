
### Train

`python main.py --upscale_factor 3 --batchSize 4 --testBatchSize 100 --nEpochs 30 --lr 0.001`

### Super Resolve
`python super_resolve.py --input_image dataset/BSDS300/images/test/16077.jpg --model model_epoch_500.pth --output_filename out.png`

### В этом примере обучается сеть со сверхвысоким разрешением на наборе данных BSD300 , используя кадры из 200 обучающих изображений и оценивая кадры из 100 тестовых изображений. Снимок модели после каждой эпохи с именем файла model_epoch_ <epoch_number> .pth