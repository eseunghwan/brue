
// base functions(like python)
function enumerate(source) {
    var enums = [];
    if (typeof(source) == "object") {
        var idx = 0;
        for (var key in source) {
            enums.push([ idx, key, source[key] ]);
            idx += 1;
        }
    }
    else {
        var idx = 0;
        for (var item of source) {
            enums.push([ idx, item ]);
            idx += 1;
        }
    }

    return enums;
}

// base functions(type casts)
function int(source) {
    try {
        return parseInt(source);
    }
    catch {
        return source;
    }
}

function float(source) {
    try {
        return parseFloat(source);
    }
    catch {
        return source;
    }
}

function bool(source) {
    try {
        return Boolean(source);
    }
    catch {
        return source;
    }
}

function str(source) {
    try {
        return toString(source);
    }
    catch {
        return source;
    }
}

function list(source) {
    return source;
}

function dict(source) {
    return source;
}

// decorators
function defineElement(tag_name) {
    return (cls) => {
        window.customElements.define(tag_name, cls);
        Object.defineProperty(cls, "tag_name", {"value": tag_name, "enumerable": false, "configurable": false, "writable": false});

        return cls;
    };
};

// directives
function repeat(iterable, iter_method) {
    var templates = [];
    
    if (typeof(iterable) == "object" && !(iterable instanceof Array) && !(iterable instanceof Date)) {
        // convert to list if dictionary
        var iterable_array = [];
        for (var key of Object.getOwnPropertyNames(iterable)) {
            iterable_array.push([ key, iterable[key] ]);
        }

        iterable = iterable_array;
    }

    for (var iter_item of iterable) {
        try {
            templates.push(iter_method(...iter_item));
        }
        catch {
            templates.push(iter_method(iter_item));
        }
    }

    return templates.join("\n")
};

// core classes
var brue = {
    routes: {},
    store: {},
    use(cls) {
        if (cls["type"] != undefined) {
            var cls_type = cls["type"];
            delete cls["type"];
            if (cls_type == "brueStore") {
                brue.store = cls;
            }
            else if (cls_type == "brueRoute") {
                brue.routes = {};
                for (var item of cls["info"]) {
                    brue.routes[item["path"]] = item["component"].tag_name;
                }
            }
        }
    }
};

function brueStore(kwargs) {
    kwargs["type"] = "brueStore";
    return kwargs;
}

function brueRoute(router_infos) {
    return {
        type: "brueRoute",
        info: router_infos
    };
}

class brueElement extends HTMLElement {
    constructor() {
        super();

        this.created();

        this.$route_view = null;
        this.$focus_address = [];
        this.store = brue.store;
        this.$props = this.props == undefined ? {} : this.props;
        if (this.state == undefined) {
            this.state = {};
        }
        this.refs = {};

        this.attachShadow({ mode: "open" });
    }

    $get_focus_address(element) {
        this.$focus_address.unshift(Array.prototype.indexOf.call(element.parentNode.children, element));

        if (element.parentNode != this.shadowRoot) {
            this.$get_focus_address(element.parentNode);
        }
    }

    $get_from_model_names(model_names) {
        var model = this;
        for (var name of model_names) {
            model = model[name];
        }

        return model;
    }

    $set_to_model_names(model_names, value) {
        var model_value = this.$get_from_model_names(model_names);

        if (typeof(model_value) == "number") {
            if (model_value % 1 == 0) {
                value = parseInt(value);
            }
            else {
                value = parseFloat(value);
            }
        }
        else if (typeof(model_value) == "string") {
            value = `"${value}"`;
        }
        else {
            try {
                value = eval(value);
            }
            catch {}
        }

        eval(`this.${model_names.join(".")} = ${value}`);
    }

    $find_element_custom_attr(element) {
        var has_custom_attr = false;
        for (var idx = 0; idx < element.attributes.length; idx++) {
            var key = element.attributes[idx].name;
            if (key.startsWith(":")) {
                has_custom_attr = true;
                break;
            }
        }

        Object.defineProperty(element, "root", {"value": this, "enumerable": false, "configurable": false, "writable": false});
        if (element.tagName == "ROUTER-VIEW") {
            this.$route_view = element;
        }
        element.addEventListener("focus", (ev) => {
            ev.target.root.$focus_address = [];
            ev.target.root.$get_focus_address(ev.target);
        });

        if (has_custom_attr) {
            if (element.hasAttribute("ref")) {
                this.refs[element.getAttribute("ref")] = element;
                element.removeAttribute("ref");
            }

            this.$connect_event(element);
            this.$connect_model(element);
        }

        for (var child of element.children) {
            this.$find_element_custom_attr(child);
        }
    }

    $connect_event(element) {
        var self = this;
        for (var idx = 0; idx < element.attributes.length; idx++) {
            var key = element.attributes[idx].name;
            if (key.startsWith(":on-")) {
                var func = eval(element.attributes[idx].value);
                element.removeAttribute(key);
                element.addEventListener(key.substring(4), func.bind(this));
            }
        }
    }

    $connect_model(element) {
        var self = this;
        for (var idx = 0; idx < element.attributes.length; idx++) {
            var key = element.attributes[idx].name;
            if (key == ":model") {
                var model_name = element.attributes[idx].value;
                var model_names = [];
                if (model_name.startsWith("self.")) {
                    model_names = model_name.substring(5).split(".");
                }
                else {
                    model_names = model_name.split(".");
                }

                element.removeAttribute(key);
                element.value = this.$get_from_model_names(model_names);

                Object.defineProperty(element, "model_names", {"value": model_names, "enumerable": false, "configurable": false, "writable": false});
                element.addEventListener("change", (ev) => {
                    ev.target.root.$set_to_model_names(ev.target.model_names, ev.target.value);
                });
            }
        }
    }

    connectedCallback() {
        this.mounted();

        var self = this;
        var props = {}, state = {};
        for (var key in this.$props) {
            if (this.hasAttribute(key)) {
                props[key] = this.getAttribute(key);
            }
        }
        this.props = props;

        for (var key in this.state) {
            state[key] = this.state[key];
        }

        this.state = new Proxy(state, {
            get(t, n, r) {
                return Reflect.get(t, n, r);
            },
            set(t, n, r) {
                var res = Reflect.set(t, n, r);
                self.$update();

                return res;
            }
        });

        this.$update();
    }

    $update() {
        this.shadowRoot.innerHTML = this.render();
        if (this.constructor.css_string != undefined) {
            var style_elm = document.createElement("style");
            style_elm.setAttribute("type", "text/css");
            style_elm.appendChild(document.createTextNode(this.constructor.css_string));

            this.shadowRoot.appendChild(style_elm);
        }
        this.$find_element_custom_attr(this.shadowRoot.firstElementChild);

        var focus_elm = this.shadowRoot;
        for (var address of this.$focus_address) {
            focus_elm = focus_elm.children[address];
        }

        if (focus_elm != this.shadowRoot) {
            focus_elm.focus();
        }
    }

    created() {}

    mounted() {}

    render() {}
};


// custom elements
// routers
class RouterLink extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    connectedCallback() {
        this.$text = this.firstChild.nodeValue;

        this.$url = this.getAttribute("url");
        this.removeAttribute("url");

        var link = document.createElement("a");
        link.href = "#";
        link.innerText = this.firstChild.nodeValue;
        link.addEventListener("click", (ev) => {
            this.root.$route_view.change_view(this.$url);
        })
        this.shadowRoot.appendChild(link);
        this.removeChild(this.firstChild);
    }
}
window.customElements.define("router-link", RouterLink);

class RouterView extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    connectedCallback() {
        this.change_view("/");
    }

    change_view(view_url) {
        if (brue.routes.hasOwnProperty(view_url)) {
            var tag_name = brue.routes[view_url];
            var elm = document.createElement(tag_name);

            this.shadowRoot.innerHTML = "";
            this.shadowRoot.appendChild(elm);
        }
    }
}
window.customElements.define("router-view", RouterView);

