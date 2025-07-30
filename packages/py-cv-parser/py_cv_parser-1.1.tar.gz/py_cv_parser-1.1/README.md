<p align="center">
    <img src="https://raw.githubusercontent.com/Hunnyisme/image_library/refs/heads/master/cvparserlogo.png" alt="" style="width:60%; height:300px"></imag></p>


<h1 align="center"> CVPARSRR </h1>

<p align="center">
    <img alt="Static Badge" src="https://img.shields.io/badge/license-Apache2.0-blue">
    <img alt="Static Badge" src="https://img.shields.io/badge/version-1.0-orange"></p>



<p>	A powerful resume analysis tool based on a NLP model. It is easy-to-use and reusable.
You can extract critical information from a resume by this tool.</p>
<h2>
Install
</h2>

please use this command to install:

```
pip install py-cv-parser
```

Also need to install this NLP model:

```
pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.8.0/en_core_web_trf-3.8.0-py3-none-any.whl#sha256=272a31e9d8530d1e075351d30a462d7e80e31da23574f1b274e200f3fff35bf5"
```



<h2>
How to use    
</h2>

Load a resume file

```
parser=CvParser.load("your_file_path")
```

Get the raw information from a resume file

```
doc=parser.parse()
```

Then, analyze and extract information 

```
the_cv=ExtractorFactory.get_extractor(doc,'Australia').extract() # The second parameter is the country of the resume.
```

Finally,  you can check those information.

```
print(the_cv) #check all items
```

Check single item

```
print(the_cv.skills)
print(the_cv.name)
```



<h2>
Notice
</h2>

This project has a huge space to improve so far. It only supports an lanugage type of English and a file type of PDF. I will keep updating it and welcome anyone to join.

