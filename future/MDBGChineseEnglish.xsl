<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng"
				version="1.0">
<xsl:output method="xml" encoding="UTF-8" indent="no"
	doctype-public="-//W3C//DTD XHTML 1.1//EN"
	doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />

<!--
	Entry tag
-->
<xsl:template match="d:entry">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()" />
	</xsl:copy>
	<style type="text/css">
		body > div:after {
			display: block;
			content: "MDBG.NET";
			text-align: right;
			font-size: 75%;
		}
	
		<xsl:if test="$tonecolors = '1'">
			.mpt1
			{
				color: #ff0000	!important;
			}
			.mpt2
			{
				color: #f0a800	!important;
			}
			.mpt3
			{
				color: #00a000	!important;
			}
			.mpt4
			{
				color: #0000ff	!important;
			}
			.mpt5
			{
				color: #000000	!important;
			}
			.mptd
			{
				color: #a0a0a0	!important;
			}
		</xsl:if>
		<xsl:if test="$tonecolors = '2'">
			.mpt1
			{
				color: #dd0000	!important;
			}
			.mpt2
			{
				color: #00aa00	!important;
			}
			.mpt3
			{
				color: #0000ff	!important;
			}
			.mpt4
			{
				color: #cc32ff	!important;
			}
			.mpt5
			{
				color: #777777	!important;
			}
			.mptd
			{
				color: #000000	!important;
			}
		</xsl:if>
		<xsl:if test="$tonecolors = '3'">
			<xsl:if test="$mptc1 = '0'">
				.mpt1
				{
					color: #dd0000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '1'">
				.mpt1
				{
					color: #f0a800	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '2'">
				.mpt1
				{
					color: #00a000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '3'">
				.mpt1
				{
					color: #0000ff	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '4'">
				.mpt1
				{
					color: #000000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '5'">
				.mpt1
				{
					color: #a0a0a0	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '6'">
				.mpt1
				{
					color: #777777	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '7'">
				.mpt1
				{
					color: #964b00	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '8'">
				.mpt1
				{
					color: #ffa6c9	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc1 = '9'">
				.mpt1
				{
					color: #cc32ff	!important;
				}
			</xsl:if>


			<xsl:if test="$mptc2 = '0'">
				.mpt2
				{
					color: #dd0000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '1'">
				.mpt2
				{
					color: #f0a800	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '2'">
				.mpt2
				{
					color: #00a000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '3'">
				.mpt2
				{
					color: #0000ff	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '4'">
				.mpt2
				{
					color: #000000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '5'">
				.mpt2
				{
					color: #a0a0a0	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '6'">
				.mpt2
				{
					color: #777777	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '7'">
				.mpt2
				{
					color: #964b00	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '8'">
				.mpt2
				{
					color: #ffa6c9	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc2 = '9'">
				.mpt2
				{
					color: #cc32ff	!important;
				}
			</xsl:if>


			<xsl:if test="$mptc3 = '0'">
				.mpt3
				{
					color: #dd0000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '1'">
				.mpt3
				{
					color: #f0a800	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '2'">
				.mpt3
				{
					color: #00a000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '3'">
				.mpt3
				{
					color: #0000ff	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '4'">
				.mpt3
				{
					color: #000000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '5'">
				.mpt3
				{
					color: #a0a0a0	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '6'">
				.mpt3
				{
					color: #777777	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '7'">
				.mpt3
				{
					color: #964b00	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '8'">
				.mpt3
				{
					color: #ffa6c9	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc3 = '9'">
				.mpt3
				{
					color: #cc32ff	!important;
				}
			</xsl:if>


			<xsl:if test="$mptc4 = '0'">
				.mpt4
				{
					color: #dd0000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '1'">
				.mpt4
				{
					color: #f0a800	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '2'">
				.mpt4
				{
					color: #00a000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '3'">
				.mpt4
				{
					color: #0000ff	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '4'">
				.mpt4
				{
					color: #000000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '5'">
				.mpt4
				{
					color: #a0a0a0	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '6'">
				.mpt4
				{
					color: #777777	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '7'">
				.mpt4
				{
					color: #964b00	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '8'">
				.mpt4
				{
					color: #ffa6c9	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc4 = '9'">
				.mpt4
				{
					color: #cc32ff	!important;
				}
			</xsl:if>


			<xsl:if test="$mptc5 = '0'">
				.mpt5
				{
					color: #dd0000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '1'">
				.mpt5
				{
					color: #f0a800	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '2'">
				.mpt5
				{
					color: #00a000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '3'">
				.mpt5
				{
					color: #0000ff	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '4'">
				.mpt5
				{
					color: #000000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '5'">
				.mpt5
				{
					color: #a0a0a0	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '6'">
				.mpt5
				{
					color: #777777	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '7'">
				.mpt5
				{
					color: #964b00	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '8'">
				.mpt5
				{
					color: #ffa6c9	!important;
				}
			</xsl:if>
			<xsl:if test="$mptc5 = '9'">
				.mpt5
				{
					color: #cc32ff	!important;
				}
			</xsl:if>


			<xsl:if test="$mptcd = '0'">
				.mptd
				{
					color: #dd0000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '1'">
				.mptd
				{
					color: #f0a800	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '2'">
				.mptd
				{
					color: #00a000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '3'">
				.mptd
				{
					color: #0000ff	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '4'">
				.mptd
				{
					color: #000000	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '5'">
				.mptd
				{
					color: #a0a0a0	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '6'">
				.mptd
				{
					color: #777777	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '7'">
				.mptd
				{
					color: #964b00	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '8'">
				.mptd
				{
					color: #ffa6c9	!important;
				}
			</xsl:if>
			<xsl:if test="$mptcd = '9'">
				.mptd
				{
					color: #cc32ff	!important;
				}
			</xsl:if>
		</xsl:if>
	
		<xsl:if test="$cantonese = '0'">
			.caj { display: none; }
		</xsl:if>
		<xsl:if test="$cantonese = '1'">
			.cay { display: none; }
		</xsl:if>
	
		<xsl:if test="$pronunciation = '0'">
			.pytm { display: none; }
			.bpmf { display: none; }
		</xsl:if>
		<xsl:if test="$pronunciation = '1'">
			.pytn { display: none; }
			.bpmf { display: none; }
		</xsl:if>
		<xsl:if test="$pronunciation = '2'">
			.pytn { display: none; }
			.pytm { display: none; }
		</xsl:if>

		<xsl:if test="$chardetails = '0'">
			.cd { display: none; }
		</xsl:if>
	</style>
</xsl:template>

<!--
	Default rule for all other tags
-->
<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()" />
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>
