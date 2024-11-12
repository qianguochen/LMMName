## 一、Operating Environment

* operating system： centos7
* development environment： Java8 python 3.7

## 二、Extract Data Set

* prepare the experimental project
* modify the parameters of the configuration file config.ini
  * parameter: DATA\_SAVE\_DIR (experimental data saving path)
  * parameter: PROJECT\_DIR (experimental project save path)
* run the process.sh to extract the data set

## 三、Get GPT Results

* modify the parameters of the configuration file config.ini
  * parameter: key (gpt key)
  * parameter: url (gpt request path)
* run the GPT.sh

## 四、GPT results were analyzed

### Preliminary judgment

* run the tagger.sh to pre-process the result

### Manual analysis of the original method and GPT prediction method is superior

* run the judgement.sh to determine the method that is not confirmed

## 五、Statistics Of Experimental Results

* run the calculate.sh to calculate the experiment result

