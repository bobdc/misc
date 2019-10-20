<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="xml" omit-xml-declaration="yes"  indent="no"/>

    <xsl:template match="script|style|meta|link|div[@id='mw-navigation']|div[@class='printfooter']|div[@id='catlinks']|div[@id='footer']|div[@id='siteSub']|a[@class='mw-jump-link']|span[@class='mw-editsection']"/>

    <xsl:template match="h1">
     <title><xsl:value-of select='.'/></title>
    </xsl:template>
    
    <xsl:template match="link[@rel='canonical']">
     <url><xsl:value-of select='@href'/></url>
    </xsl:template>
    
        <xsl:template match="td|th">
      <xsl:value-of select='.'/><xsl:text> </xsl:text>
    </xsl:template>

    <!--
    <xsl:template match="script[@type='application/ld+json']">
      <xsl:value-of select='.'/>
    </xsl:template>

    <xsl:template match ="text()"/>
    -->
</xsl:stylesheet>
