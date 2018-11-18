Record the experience I install the Brian2
===
I install Brian2 with Anaconda in Windows 10(64 bit). At first, it was a really hard work for me that I failed for times. To be frankly, I am not good at doing this things like configuring environments etc. So I will only record how I install it sucessfully. 

Simply put that there are only two steps: 
1. Set up Anaconda.
2. Install the Brian2 through conda.<br>

**The more details will be seen in the** [Brian2's installation guide.](https://brian2.readthedocs.io/en/stable/introduction/install.html)
## 1.Set up Anaconda.<br>
Please refer to the [installation guide](https://docs.anaconda.com/anaconda/install/).
In this part, there is no problem generally, one point you should know that do not install it in a Chinese directory.(不要在中文路径下安装)

## 2. Install the Brain2 through conda.
At first, I install the Brian2 in the default `base` environment, however, it could not work when I test it in `Spyder` or `Anaconda prompt`.<br>
So I create a new environment for the Brian2.
### (1)Create a new environment for the Brian2.
* Open the `Anaconda prompt` from the start menu.
* Type the code:<br>
`conda create --name brianenv biopython`<br>
then type<br>
`activate brianenv`<br>
We enter the new environment `brianenv`,and we can install the `Brian2`.<br>
`conda install -c brian-team brian2 `<br>
or<br>
`conda install brian2`
Done!<br>
We could test it now.In `Anaconda prompt`, we should enter the new environment for brian2 through type the code:<br>
`activate brianenv`<br>
In the `brianenv` environment, we should use python, so type:<br>
`python`<br>
Then the arrow sign changes into `>>>`, we type:<br>
`import brian2`.<br>
If print nothing, the installation is successfull.

### (2)Use the brian2 in Spyder
Now, you should recreate a Spyder terminal for `brianenv`.<br>
* Open the `Anaconda navigator`. Choose `Environments`, here list the environments you created.
![](https://github.com/HardworkingChris/Brian2_Learning/1-install/raw/master/install1.png)  
* Choose `brianenv`, click the bar showing 'Installed' or something, from which we choose `all`. Find `Spyder` and choose it, then you can click the `Apply` button in the right-bottom side to install the `Spyder(brianenv)`.
![](https://github.com/HardworkingChris/Brian2_Learning/1-install/raw/master/install2.png) 
![](https://github.com/HardworkingChris/Brian2_Learning/1-install/raw/master/install3.png) 
* From the start menu, you will see the new spyder named `Spyder(brianenv)`, click it.<br>

Then everthing is OK!.
