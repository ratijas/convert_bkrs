<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng"
				version="1.0"
				result-ns="">
 <xsl:output method="xml" encoding="UTF-8" indent="no"
	doctype-public="-//W3C//DTD XHTML 1.1//EN"
	doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />


<xsl:template match="d:entry">
	<div id="btn" style="float: right">
	</div>
	<xsl:copy>
		<xsl:apply-templates select="@*|node()" />
	</xsl:copy>

<!-- 
var themes = {
	"none" : 0,
	"mandarin" : 1,
	"cc_cedict" : 2,
	"pleco" : 3,
	"bw" : 4,
	"custom" : 5
};
 -->
	<style type="text/css">
		<xsl:if test="$color_mode = '1'">
			.t0 {color:#696969}
			.t1 {color:#FE8E37}
			.t2 {color:#61c538}
			.t3 {color:#427DF7}
			.t4 {color:#f94229}
		</xsl:if>
		<xsl:if test="$color_mode = '2'">
			.t0 {color:#696969}
			.t1 {color:#f94229}
			.t2 {color:#FE8E37}
			.t3 {color:#61c538}
			.t4 {color:#427DF7}
		</xsl:if>
		<xsl:if test="$color_mode = '3'">
			.t0 {color:#696969}
			.t1 {color:#f94229}
			.t2 {color:#61c538}
			.t3 {color:#8780f7}
			.t4 {color:#ec8af9}
		</xsl:if>
		<xsl:if test="$color_mode = '4'">
			.t0 {color:#696969}
			.t1 {color:#000}
			.t2 {color:#000}
			.t3 {color:#000}
			.t4 {color:#000}
		</xsl:if>
		<xsl:if test="$color_mode = '5'">
			.t0 {
				<xsl:if test="$tc0 = '0'">
					color: #dd0000;
				</xsl:if>
				<xsl:if test="$tc0 = '1'">
					color: #f0a800;
				</xsl:if>
				<xsl:if test="$tc0 = '2'">
					color: #00a000;
				</xsl:if>
				<xsl:if test="$tc0 = '3'">
					color: #0000ff;
				</xsl:if>
				<xsl:if test="$tc0 = '4'">
					color: #000000;
				</xsl:if>
				<xsl:if test="$tc0 = '5'">
					color: #a0a0a0;
				</xsl:if>
				<xsl:if test="$tc0 = '6'">
					color: #777777;
				</xsl:if>
				<xsl:if test="$tc0 = '7'">
					color: #964b00;
				</xsl:if>
				<xsl:if test="$tc0 = '8'">
					color: #ffa6c9;
				</xsl:if>
				<xsl:if test="$tc0 = '9'">
					color: #cc32ff;
				</xsl:if>
			}
			.t1 {
				<xsl:if test="$tc1 = '0'">
					color: #dd0000;
				</xsl:if>
				<xsl:if test="$tc1 = '1'">
					color: #f0a800;
				</xsl:if>
				<xsl:if test="$tc1 = '2'">
					color: #00a000;
				</xsl:if>
				<xsl:if test="$tc1 = '3'">
					color: #0000ff;
				</xsl:if>
				<xsl:if test="$tc1 = '4'">
					color: #000000;
				</xsl:if>
				<xsl:if test="$tc1 = '5'">
					color: #a0a0a0;
				</xsl:if>
				<xsl:if test="$tc1 = '6'">
					color: #777777;
				</xsl:if>
				<xsl:if test="$tc1 = '7'">
					color: #964b00;
				</xsl:if>
				<xsl:if test="$tc1 = '8'">
					color: #ffa6c9;
				</xsl:if>
				<xsl:if test="$tc1 = '9'">
					color: #cc32ff;
				</xsl:if>
			}
			.t2 {
				<xsl:if test="$tc2 = '0'">
					color: #dd0000;
				</xsl:if>
				<xsl:if test="$tc2 = '1'">
					color: #f0a800;
				</xsl:if>
				<xsl:if test="$tc2 = '2'">
					color: #00a000;
				</xsl:if>
				<xsl:if test="$tc2 = '3'">
					color: #0000ff;
				</xsl:if>
				<xsl:if test="$tc2 = '4'">
					color: #000000;
				</xsl:if>
				<xsl:if test="$tc2 = '5'">
					color: #a0a0a0;
				</xsl:if>
				<xsl:if test="$tc2 = '6'">
					color: #777777;
				</xsl:if>
				<xsl:if test="$tc2 = '7'">
					color: #964b00;
				</xsl:if>
				<xsl:if test="$tc2 = '8'">
					color: #ffa6c9;
				</xsl:if>
				<xsl:if test="$tc2 = '9'">
					color: #cc32ff;
				</xsl:if>
			}
			.t3 {
				<xsl:if test="$tc3 = '0'">
					color: #dd0000;
				</xsl:if>
				<xsl:if test="$tc3 = '1'">
					color: #f0a800;
				</xsl:if>
				<xsl:if test="$tc3 = '2'">
					color: #00a000;
				</xsl:if>
				<xsl:if test="$tc3 = '3'">
					color: #0000ff;
				</xsl:if>
				<xsl:if test="$tc3 = '4'">
					color: #000000;
				</xsl:if>
				<xsl:if test="$tc3 = '5'">
					color: #a0a0a0;
				</xsl:if>
				<xsl:if test="$tc3 = '6'">
					color: #777777;
				</xsl:if>
				<xsl:if test="$tc3 = '7'">
					color: #964b00;
				</xsl:if>
				<xsl:if test="$tc3 = '8'">
					color: #ffa6c9;
				</xsl:if>
				<xsl:if test="$tc3 = '9'">
					color: #cc32ff;
				</xsl:if>
			}
			.t4 {
				<xsl:if test="$tc4 = '0'">
					color: #dd0000;
				</xsl:if>
				<xsl:if test="$tc4 = '1'">
					color: #f0a800;
				</xsl:if>
				<xsl:if test="$tc4 = '2'">
					color: #00a000;
				</xsl:if>
				<xsl:if test="$tc4 = '3'">
					color: #0000ff;
				</xsl:if>
				<xsl:if test="$tc4 = '4'">
					color: #000000;
				</xsl:if>
				<xsl:if test="$tc4 = '5'">
					color: #a0a0a0;
				</xsl:if>
				<xsl:if test="$tc4 = '6'">
					color: #777777;
				</xsl:if>
				<xsl:if test="$tc4 = '7'">
					color: #964b00;
				</xsl:if>
				<xsl:if test="$tc4 = '8'">
					color: #ffa6c9;
				</xsl:if>
				<xsl:if test="$tc4 = '9'">
					color: #cc32ff;
				</xsl:if>
			}
		</xsl:if>
	</style>

	<!-- добавим красок жизни? -->
	<!--
		так как специальные символы заменяются на "сущности"
		приходится пихать скрипт в блок, считывать как .innerText
		и затем исполнять eval()
	-->
	<!-- небольшая поправка: выпилен фильтр -->
	<xsl:if test="$color_mode != '0'">
		<div id="color-script" style="display:none;">
<![CDATA[
/* onDomReady() */
(function (window){var r='',d=false;var y=function(f){if(!d){var o=r; if(typeof r!='function')r=f;else{r=function(){o();f()}}}else{if(typeof f=='function')f()}};window.onDomReady=y;function init(){if(arguments.callee.done)return;arguments.callee.done=true;if(r)r();d=true};if(document.addEventListener)document.addEventListener('DOMContentLoaded',init,false);if(/WebKit/i.test(navigator.userAgent)){var _t=setInterval(function(){if(/loaded|complete/.test(document.readyState)){clearInterval(_t);init()}},10)}window.onload=init})(window);
function searchForTextNodeIn(e,t,n){n=n||[];var r=e.childNodes;var i=r.length;for(var s=0;s<i;++s){var o=r[s];if(o.nodeType==1){tagName=o.tagName.toLowerCase();if(tagName==="script"||tagName==="style"||!!t&&!t(o)){continue}searchForTextNodeIn(o,t,n)}else if(o.nodeType==3){if(o.textContent.match(/^\s*$/)!=null){continue}n.push(o)}}return n}function skip(e,t){pyPlainLength=t.length;var n=/\W/;while(e<pyPlainLength&&!t[e].match(n)){++e}while(e<pyPlainLength&&t[e].match(n)){++e}return e}function searchForPinYinInString(e){var t={};var n=e.toLowerCase().replace(/[āáǎăà]/g,"a").replace(/[ēéěè]/g,"e").replace(/[ōóǒò]/g,"o").replace(/[ūúǔù]/g,"u").replace(/[ǖǘǚǜ]/g,"u").replace(/[īíǐì]/g,"i");var r=n.length;for(var i=0;i<r;){var s=n.charCodeAt(i);if(s<97||s>122){++i;continue}var o=null;var u=null;for(var a=0;a<allPinYinListLength;++a){o=allPinYinList[a];if(n.substring(i,i+o.length)==o){var f=n[i+o.length];if(f==="a"||f==="o"||f==="e"||f==="u"||f==="i"){g=o.substring(0,o.length-1);if(allPinYinList.indexOf(g)!==-1){o=g}else{console.log('нужен апостроф в пиньине: '+o)}}u=o;break}}if(u){var l=u.length;t[new Number(i)]=e.slice(i,i+l);i+=u.length}else{i=skip(i,n)}}return t}function determineTone(e){if(e.match(/[āēūǖīō]/))return 1;if(e.match(/[áéúǘíó]/))return 2;if(e.match(/[ǎăěǔǚǐǒ]/))return 3;if(e.match(/[àèùǜìò]/))return 4;return 0}function colorizePinYin(e,t){if(plainTextNodesList.indexOf(e)!=-1){return}var n=true;var r={};for(start in t){var i=determineTone(t[start]);r[start]=i;if(i!=0){n=false}}if(n){return}var s=document.createElement("span");s.classList.add("pinYinWrapper");var o=null;var u=e.textContent;for(start in t){start=new Number(start);s.appendChild(document.createTextNode(u.slice(o!=null?o:0,start)));var a=document.createElement("span");var f=r[start];a.classList.add("t"+f);a.appendChild(document.createTextNode(t[start]));s.appendChild(a);o=start+t[start].length}s.appendChild(document.createTextNode(u.slice(o)));plainTextNodesList.push(e);colorizedTextNodesList[plainTextNodesList.length-1]=s}(function(e){function i(){if(arguments.callee.done)return;arguments.callee.done=true;if(t)t();n=true}var t="",n=false;var r=function(e){if(!n){var r=t;if(typeof t!="function")t=e;else{t=function(){r();e()}}}else{if(typeof e=="function")e()}};e.onDomReady=r;if(document.addEventListener)document.addEventListener("DOMContentLoaded",i,false);if(/WebKit/i.test(navigator.userAgent)){var s=setInterval(function(){if(/loaded|complete/.test(document.readyState)){clearInterval(s);i()}},10)}e.onload=i})(window);var plainTextNodesList=[];var colorizedTextNodesList=[];window.onDomReady(function(){var e=document.querySelector("body");var t=searchForTextNodeIn(e,null);var n=t.length;for(var r=0;r<n;++r){textNode=t[r];var i=searchForPinYinInString(textNode.textContent);if(Object.keys(i).length==0){continue}colorizePinYin(textNode,i)}colorizeAllPinYin(true)});var allPinYinList="zhuang,shuang,chuang,zhuan,zhuai,zhong,zheng,zhang,xiong,xiang,shuan,shuai,sheng,shang,qiong,qiang,niang,liang,kuang,jiong,jiang,huang,guang,chuan,chuai,chong,cheng,chang,zuan,zong,zhuo,zhun,zhui,zhua,zhou,zhen,zhei,zhao,zhan,zhai,zeng,zang,yuan,yong,ying,yang,xuan,xing,xiao,xian,weng,wang,tuan,tong,ting,tiao,tian,teng,tang,suan,song,shuo,shun,shui,shua,shou,shen,shei,shao,shan,shai,seng,sang,ruan,rong,reng,rang,quan,qing,qiao,qian,ping,piao,pian,peng,pang,nüe,nuan,nong,ning,niao,nian,neng,nang,ming,miao,mian,meng,mang,lüe,luan,long,ling,liao,lian,leng,lang,kuan,kuai,kong,keng,kang,juan,jing,jiao,jian,huan,huai,hong,heng,hang,guan,guai,gong,geng,gang,feng,fang,duan,dong,ding,diao,dian,deng,dang,cuan,cong,chuo,chun,chui,chua,chou,chen,chao,chan,chai,ceng,cang,bing,biao,bian,beng,bang,zuo,zun,zui,zou,zhu,zhi,zhe,zha,zen,zei,zao,zan,zai,yun,yue,you,yin,yao,yan,xun,xue,xiu,xin,xie,xia,wen,wei,wan,wai,tuo,tun,tui,tou,tie,tao,tan,tai,suo,sun,sui,sou,shu,shi,she,sha,sen,sei,sao,san,sai,ruo,run,rui,rua,rou,ren,rao,ran,qun,que,qiu,qin,qie,qia,pou,pin,pie,pen,pei,pao,pan,pai,nü,nuo,nou,niu,nin,nie,nen,nei,nao,nan,nai,mou,miu,min,mie,men,mei,mao,man,mai,lü,luo,lun,lou,liu,lin,lie,lia,lei,lao,lan,lai,kuo,kun,kui,kua,kou,ken,kei,kao,kan,kai,jun,jue,jiu,jin,jie,jia,huo,hun,hui,hua,hou,hng,hen,hei,hao,han,hai,guo,gun,gui,gua,gou,gen,gei,gao,gan,gai,fou,fen,fei,fan,duo,dun,dui,dou,diu,die,den,dei,dao,dan,dai,dia,cuo,cun,cui,cou,chu,chi,che,cha,cen,cei,cao,can,cai,bin,bie,ben,bei,bao,ban,bai,ang,ê,zu,zi,ze,za,yu,yi,ye,ya,xu,xi,wu,wo,wa,tu,ti,te,ta,su,si,se,sa,ru,ri,re,qu,qi,pu,po,pi,pa,ou,nu,ni,ng,ne,na,mu,mo,mi,ma,me,lu,li,le,la,ku,ke,ka,ju,ji,hu,hm,he,ha,gu,ge,ga,fu,fo,fa,er,en,ei,du,di,de,da,cu,ci,ce,ca,bu,bo,bi,ba,ao,an,ai,yo,o,n,m,e,a".split(",");var allPinYinListLength=allPinYinList.length;(function(){var e=null;window.colorizeAllPinYin=function(t){if(typeof (t=!!t)!=="boolean"||e===t)return;e=t;var n,r;if(t){n=plainTextNodesList;r=colorizedTextNodesList}else{n=colorizedTextNodesList;r=plainTextNodesList}for(var i=n.length-1;i>=0;i--){var s=n[i];var o=s.parentNode;o.insertBefore(r[i],s);o.removeChild(s)}}})();(function(e){var t="#000",n="#696969";red="#f94229",green="#61c538",violet="#8780f7",pink="#ec8af9",blue="#427DF7",orange="#FE8E37";var r={none:null,"b&w":[n,t,t,t,t],pleco:[n,red,green,violet,pink],"cc-cedict":[n,red,orange,green,blue],mandarin:[n,orange,green,blue,red]};e.addTheme=function(e,t){if(t.length!==5)return null;r[e]=t};getColorsForTheme=function(e){var t=r[e];return t?t:null};var i="ColorizeStyleID";e.connectStylesheet=function(e){var t=getColorsForTheme(e);if(!t){return}var n,r;if(!(n=document.getElementById(i))){n=document.createElement("style");n.id=i;n.type="text/css";document.querySelector("head").appendChild(n)}n.textContent="";r="";for(var s=0;s<=4;++s){r+=".t"+s+"{color:"+t[s]+"} "}n.textContent=r}})(window);

// кнопки просмотра и правки на сайте
window.onDomReady(function(){
	var h1 = document.querySelector('h1');
	if ( h1.innerText == 'обложка 大БКРС / БРуКС' ) return;
	
	var template = 
'<style scoped>'+
'	a, a > img {padding: 0; margin: 0}'+
'	a {display: inline; text-decoration: none;}'+
'	a > img {width: 32px; height: 32px;}'+
'</style>'+
'<a href="http://bkrs.info/form.php?{{lang}}={{word}}" title="править слово" style="padding-right: 15px; margin-left: 12px;">'+
'	<img src="Images/pencil.png" alt="править слово">'+
'</a>'+
'<a href="http://bkrs.info/slovo.php?ch={{word}}" title="открыть на сайте bkrs.info">'+
'	<img src="Images/browse.png" alt="открыть на сайте bkrs.info">'+
'</a>',
	final = template
		.replace( /{{word}}/g, document.querySelector('h1').innerText )
		.replace( /{{lang}}/g, ( document.querySelector( 'div.py' )) ? 'chw' : 'ruw' );
	document.querySelector('#btn').innerHTML += final;
});
]]>
		</div>
		<!-- выполнить -->
		<script type="text/javascript">
			t = document.querySelector('#color-script').innerText;
			window.eval( t );
		</script>
	</xsl:if>
</xsl:template>

<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()" />
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>
