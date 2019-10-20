<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <!-- xsltproc -html getRecipeList.xsl ~/temp/recipes.html -->
  
  <xsl:output method="text" indent="no"/>

  <xsl:template match="/">
    <xsl:apply-templates select=".//div[@id='mw-content-text']"/>
  </xsl:template>

  <xsl:template match="a">
wget <xsl:value-of select="@href"/>
  </xsl:template>

  <xsl:template match="h2|text()"/>
</xsl:stylesheet>
