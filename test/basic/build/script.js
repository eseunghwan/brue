function enumerate(source){var enums=[];if(typeof(source)=="object"){var idx=0;for(var key in source){enums.push([idx,key,source[key]]);idx+=1;}}
else{var idx=0;for(var item of source){enums.push([idx,item]);idx+=1;}}
return enums;}
function int(source){try{return parseInt(source);}
catch{return source;}}
function float(source){try{return parseFloat(source);}
catch{return source;}}
function bool(source){try{return Boolean(source);}
catch{return source;}}
function str(source){try{return toString(source);}
catch{return source;}}
function list(source){return source;}
function dict(source){return source;}
function defineElement(tag_name){return(cls)=>{window.customElements.define(tag_name,cls);Object.defineProperty(cls,"tag_name",{"value":tag_name,"enumerable":false,"configurable":false,"writable":false});return cls;};};function repeat(iterable,iter_method){var templates=[];if(typeof(iterable)=="object"&&!(iterable instanceof Array)&&!(iterable instanceof Date)){var iterable_array=[];for(var key of Object.getOwnPropertyNames(iterable)){iterable_array.push([key,iterable[key]]);}
iterable=iterable_array;}
for(var iter_item of iterable){try{templates.push(iter_method(...iter_item));}
catch{templates.push(iter_method(iter_item));}}
return templates.join("\n")};var brue={$route_view:null,routes:{},store:{},use(cls){if(cls["type"]!=undefined){var cls_type=cls["type"];delete cls["type"];if(cls_type=="brueStore"){brue.store=cls;}
else if(cls_type=="brueRoute"){brue.routes={};for(var item of cls["info"]){brue.routes[item["path"]]=item["component"].tag_name;}}}}};function brueStore(kwargs){kwargs["type"]="brueStore";return kwargs;}
function brueRoute(router_infos){return{type:"brueRoute",info:router_infos};}
class brueElement extends HTMLElement{constructor(){super();this.created();this.store=brue.store;this.$props=this.props==undefined?{}:this.props;if(this.state==undefined){this.state={};}
this.attachShadow({mode:"open"});}
$find_element_custom_attr(element){var has_custom_attr=false;for(var idx=0;idx<element.attributes.length;idx++){var key=element.attributes[idx].name;if(key.startsWith(":")){has_custom_attr=true;break;}}
if(has_custom_attr){this.$connect_event(element);}
for(var child of element.children){this.$find_element_custom_attr(child);}}
$connect_event(element){var self=this;for(var idx=0;idx<element.attributes.length;idx++){var key=element.attributes[idx].name;if(key.startsWith(":")){var func=eval(element.attributes[idx].value);element.removeAttribute(key);element.addEventListener(key.substring(1),func.bind(this));}}}
connectedCallback(){this.mounted();var self=this;var props={},state={};for(var key in this.$props){if(this.hasAttribute(key)){props[key]=this.getAttribute(key);}}
this.props=props;for(var key in this.state){state[key]=this.state[key];}
this.state=new Proxy(state,{get(t,n,r){return Reflect.get(t,n,r);},set(t,n,r){var res=Reflect.set(t,n,r);self.$update();return res;}});this.$update();}
$update(){this.shadowRoot.innerHTML=this.render();if(this.constructor.css_string!=undefined){var style_elm=document.createElement("style");style_elm.setAttribute("type","text/css");style_elm.appendChild(document.createTextNode(this.constructor.css_string));this.shadowRoot.appendChild(style_elm);}
this.$find_element_custom_attr(this.shadowRoot.firstElementChild);}
created(){}
mounted(){}
render(){}};class RouterLink extends HTMLElement{constructor(){super();this.attachShadow({mode:"open"});}
connectedCallback(){this.$text=this.firstChild.nodeValue;this.$url=this.getAttribute("url");this.removeAttribute("url");var link=document.createElement("a");link.href="#";link.innerText=this.firstChild.nodeValue;link.addEventListener("click",(ev)=>{brue.$route_view.change_view(this.$url);})
this.shadowRoot.appendChild(link);this.removeChild(this.firstChild);}}
window.customElements.define("router-link",RouterLink);class RouterView extends HTMLElement{constructor(){super();this.attachShadow({mode:"open"});brue.$route_view=this;}
connectedCallback(){this.change_view("/");}
change_view(view_url){if(brue.routes.hasOwnProperty(view_url)){var tag_name=brue.routes[view_url];var elm=document.createElement(tag_name);this.shadowRoot.innerHTML="";this.shadowRoot.appendChild(elm);}}}
window.customElements.define("router-view",RouterView);var _pj;function _pj_snippets(container){function set_class_decorators(cls,decos){function reducer(val,deco){return deco(val,cls);}
return decos.reduce(reducer,cls);}
function set_properties(cls,props){var desc,value;var _pj_a=props;for(var p in _pj_a){if(_pj_a.hasOwnProperty(p)){value=props[p];if(((((!((value instanceof Map)||(value instanceof WeakMap)))&&(value instanceof Object))&&("get"in value))&&(value.get instanceof Function))){desc=value;}else{desc={"value":value,"enumerable":false,"configurable":true,"writable":true};}
Object.defineProperty(cls.prototype,p,desc);}}}
container["set_class_decorators"]=set_class_decorators;container["set_properties"]=set_properties;return container;}
_pj={};_pj_snippets(_pj);class Hello extends brueElement{constructor(){super();}
render(){return`<h3>Hello ${this.props.name}!</h3>`;}}
_pj.set_properties(Hello,{"props":{"name":str}});Hello=_pj.set_class_decorators(Hello,[defineElement("comp-hello")]);class Counter extends brueElement{constructor(){super();}
count_up(){this.state.count+=1;}
count_down(){if((this.state.count>0)){this.state.count-=1;}}
render(){return`<div class="column"><label>clicked ${this.state.count}times!</label><div class="row"><button:click="self.count_up"style="flex:1;">up!</button><button:click="self.count_down"style="flex:1;">down!</button></div></div>`;}}
_pj.set_properties(Counter,{"state":{"count":0}});Object.defineProperty(Counter,"css_string",{"value":`.column{display:flex;flex-flow:column;}.row{display:flex;flex-flow:row;}`,"enumerable":false,"configurable":false,"writable":false});Counter=_pj.set_class_decorators(Counter,[defineElement("view-counter")]);class DataGrid extends brueElement{constructor(){super();}
render(){return`<div><table><thead>${repeat(this.state.columns,(c)=>{return`<th>${c}</th>`;})}</thead><tbody>${repeat(this.state.datas,(it)=>{return`<tr>${repeat(it,(d)=>{return`<td>${d}</td>`;})}</tr>`;})}</tbody></table></div>`;}}
_pj.set_properties(DataGrid,{"state":{"columns":["A","B","C","D"],"datas":[[1,2,3,4],[5,6,7,8]]}});Object.defineProperty(DataGrid,"css_string",{"value":`table{width:100%;border:1px solid black;border-collapse:collapse;}
thead{background-color:slategray;color:white;}
th,td{border:1px solid black;padding:5px;}
td{text-align:center;}`,"enumerable":false,"configurable":false,"writable":false});DataGrid=_pj.set_class_decorators(DataGrid,[defineElement("data-grid")]);class Welcome extends brueElement{constructor(){super();}
render(){return"\n        <comp-hello name=\"eseunghwan\"></comp-hello>\n        ";}}
Welcome=_pj.set_class_decorators(Welcome,[defineElement("view-welcome")]);var store;store=brueStore({"count_num":1});var routes;routes=brueRoute([{"path":"/","component":Welcome},{"path":"/counter","component":Counter},{"path":"/datagrid","component":DataGrid}]);brue.use(store);brue.use(routes);class App extends brueElement{constructor(){super();}
created(){console.log("created");}
mounted(){console.log("mounted");}
render(){return"\n        <div>\n            <div>\n                <router-link url=\"/\">Welcome</router-link>\n                <router-link url=\"/counter\">Counter</router-link>\n                <router-link url=\"/datagrid\">DataGrid</router-link>\n            </div>\n            <router-view />\n        </div>\n        ";}}
App=_pj.set_class_decorators(App,[defineElement("app-elm")]);