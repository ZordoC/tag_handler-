# How to install ? 


There are dependencies you need to be installed.

1. First step is to install the python dependencies in the requirements.txt using a virtual enviroment.

        python3 -m venv <name_of_env>
        source <name_of_env>/bin/activate 
        pip3 install -r requirements.txt


2. Next we need to install eflomal tool (if we wish to generate alignements)

        cd tools/eflomal 
        make
        sudo make install
        python3 setup.py install


3. Done 


# How to use ? 


## Step 1 - Genererate the alignments 



First things first, we need to generate the alignements with the eflomal tool! 

        cd ../..
        ./gen_align.py 

You can use 

        ./gen_align.py -h 

For information about the parameters.

**Note** There assumptions here:

1. You have three seperate files source_no_tags.txt and target_no_tags (both containing one sentence per line)
2. You have a pre-trained priors file to inference the new alignment more information on eflomal's [README](https://github.com/robertostling/eflomal/blob/master/README.md). 
3. The priors file should be located in the data directory

All of these files should be in under the data directory



## Step 2 - Inference on the training 

There's two new files in the working directory aligned.fwd,aligned.rev, we are only gonna use the aligned.fwd (source/target) alignment.

Now you just run:

        ./main.py 

Check:

         ./main.py -h 

You can choose where the files come from (altough I recommend having all your files in the data folder otherwise you riks breakink the tool :-) )

And an Output.txt file should appear containing the target sentences with the tags


