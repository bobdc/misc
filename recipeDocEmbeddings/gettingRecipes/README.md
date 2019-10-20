# prepping the data

Files in this directory were used to pull down the Wikibooks recipes and strip all markup. (title and url tags do get added.) 

To use these, I first saved https://en.wikibooks.org/wiki/Cookbook:Recipes as recipes.html and ran getRecipeList.xsl on it:

   xsltproc -html getRecipeList.xsl ~/temp/recipes.html > getRecipes.sh

That creates a shell script with a list of wget commands to get the individual recipes. Run that from a temp subdirectory like this: 
  
    ../getRecipes.sh
   
Run stripWikiRecipe.xsl on each file that the shell script put into the temp subdirectory and put the results in a ../data directory, then do the doc2vec stuff on those. (stripAll.sh automates this)

