# Qawafi 

 <p align="center"> 
 <img src = "https://raw.githubusercontent.com/MagedSaeed/qawafi/main/media/logo.jpg" width = "200px"/>
 </p>
 

*Qawafi قوافي* is a platform for Arabic poetry analyasis. The main idea is to create a tool that is able to analyze a given poem or list of baits by providing the following functionalities:

* Extract Arudi Style الكتابة العروضية
* Extract the closest bait to a given bait
* Extract the tafeelat تفعيلات 
* Extract the meter بحر
* Extract the qafiyah قافية 
* Extract the era and theme of a given poem 

We use deep learning for meter classification, theme and era classification. For closest bait we used our pretrained embeddings to find the closest bait using cosine similarity. 

### Training 

We use the following notebooks for training 

<table class="tg">

  <tr>
    <th class="tg-yw4l"><b>Name</b></th>
    <th class="tg-yw4l"><b>Notebook</b></th>
  </tr>
  <tr>
    <td class="tg-yw4l">Train meter classification models using Transformer </td>
    <td class="tg-yw4l">
    <a href="https://colab.research.google.com/github/MagedSaeed/qawafi/blob/main/Notebooks/meter.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" >
    </a></td>
  </tr>
  <tr>
    <td class="tg-yw4l"> Train Era classification using Bidirectional GRUs. </td>
    <td class="tg-yw4l">
    <a href="https://colab.research.google.com/github/MagedSaeed/qawafi/blob/main/Notebooks/era.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" >
    </a></td>

  </tr>

  <tr>
    <td class="tg-yw4l">Train Theme classification using Bidirectional GRUs. </td>
    <td class="tg-yw4l">
    <a href="https://colab.research.google.com/github/MagedSaeed/qawafi/blob/main/Notebooks/theme.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg"  >
    </a></td>
  </tr>

  <tr>
    <td class="tg-yw4l">Train the embedding model </td>
    <td class="tg-yw4l">
    <a href="https://colab.research.google.com/github/MagedSaeed/qawafi/blob/main/Notebooks/embedding.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg"  >
    </a></td>
  </tr>

<table>

### Testing 
You can test our modules using the following notebook <a href="https://colab.research.google.com/github/MagedSaeed/qawafi/blob/main/demo.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" width = '100px' >
</a>. 

Sample output 

```
{'arudi_style'     : [['ألاليت شعري هل أبيتنن ليلتن بجنب لغضى أزجلقلاص ننواجيا',
                     '1101011010101101011011011010110101011010110110']],
 'closest_baits'   : [[('ألاليت شعري هل أبيتن ليلة # بجنب الغضى أزجي القِلاص '
                     'النواجيا',
                     [0.38896721601486206])]],
 'closest_patterns': [('1101011010101101011011011010110101011010110110',
                       1.0,
                       'فعولنْ مفاعيلنْ فعولنْ مفاعلنْ # فعولنْ مفاعيلنْ '
                       'فعولنْ مفاعلنْ')],
 'diacritized'     : ['أَلَالَيْتُ شِعْرِي هَلْ أَبِيتَنَّ لَيْلَةً # بِجَنْبِ '
                     'الْغَضَى أَزْجِي الْقِلَاصَ النَّوَاجِيَا'],
 'era'             : ['العصر الحديث', 'العصر العثماني'],
 'meter'           : 'الطويل',
 'qafiyah'         : ('ي',
                     'قافية بحرف الروي: ي ،  زاد لها الوصل بإشباع رويها زاد لها '
                     'التأسيس'),
 'theme'           : ['قصيدة رومنسيه', 'قصيدة شوق', 'قصيدة غزل']}
```

### iOS APP 

We developed an iOS app that interacts with the server

https://user-images.githubusercontent.com/15667714/170814102-4c7da967-8009-4ed9-a5dd-047e15f05831.mp4


### Project Structure


```



├── Bohour_iOS              # iOS app 
├── demo
│   ├── bohour              # main functionalities 
│   ├── demo.py             # main demo 
│   ├── models.py           # model architectures 
│   ├── utils.py            # helper functions
│   └── diacritizer.py      # diacritization module
|
├── qawafi_server           # qawafi server for extracting main analysis
|
├── shakkelha_server        # server for diacritization
|
├── Notebooks
│   ├── theme.ipynb         # theme classification training
│   ├── era.ipynb           # era classification training
│   ├── meter.ipynb         # meter classification training
│   └── embedding.ipynb     # embedding training
├── demo.ipynb              # main demo notebook
└── README.md
```
