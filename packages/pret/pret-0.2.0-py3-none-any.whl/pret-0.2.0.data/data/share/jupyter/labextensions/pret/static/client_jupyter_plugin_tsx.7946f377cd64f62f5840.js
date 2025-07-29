(self["webpackChunkpret"] = self["webpackChunkpret"] || []).push([["client_jupyter_plugin_tsx"],{

/***/ "./client/appLoader.ts":
/*!*****************************!*\
  !*** ./client/appLoader.ts ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   makeLoadApp: () => (/* binding */ makeLoadApp)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _cborDecoder__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./cborDecoder */ "./client/cborDecoder.js");
/* harmony import */ var valtio__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! valtio */ "webpack/sharing/consume/default/valtio/valtio");
/* harmony import */ var valtio__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(valtio__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var valtio_yjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! valtio-yjs */ "webpack/sharing/consume/default/valtio-yjs/valtio-yjs");
/* harmony import */ var valtio_yjs__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(valtio_yjs__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var proxy_compare__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! proxy-compare */ "./node_modules/proxy-compare/dist/index.js");
/* harmony import */ var use_sync_external_store_shim__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! use-sync-external-store/shim */ "./node_modules/use-sync-external-store/shim/index.js");
/* harmony import */ var _org_transcrypt_runtime___WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./org.transcrypt.__runtime__ */ "./client/org.transcrypt.__runtime__.js");








window.pret_modules = window.pret || {};
window.pret_modules["org.transcrypt.__runtime__"] = _org_transcrypt_runtime___WEBPACK_IMPORTED_MODULE_6__;
Object.defineProperty(yjs__WEBPACK_IMPORTED_MODULE_3__.Doc.prototype, 'on_update', {
    value(callback) {
        this.on('update', callback);
    },
    configurable: true,
    enumerable: false,
});
Object.defineProperty(yjs__WEBPACK_IMPORTED_MODULE_3__.Doc.prototype, 'apply_update', {
    value(update) {
        yjs__WEBPACK_IMPORTED_MODULE_3__.applyUpdate(this, update);
    },
    configurable: true,
    enumerable: false,
});
// Put the global variables in the window object to allow pret stub components and stub functions to access them
window.React = (react__WEBPACK_IMPORTED_MODULE_0___default());
(react__WEBPACK_IMPORTED_MODULE_0___default().useSyncExternalStore) =
    use_sync_external_store_shim__WEBPACK_IMPORTED_MODULE_5__.useSyncExternalStore;
window.valtio = valtio__WEBPACK_IMPORTED_MODULE_2__;
valtio__WEBPACK_IMPORTED_MODULE_2__.createProxy = proxy_compare__WEBPACK_IMPORTED_MODULE_7__.createProxy;
valtio__WEBPACK_IMPORTED_MODULE_2__.getUntracked = proxy_compare__WEBPACK_IMPORTED_MODULE_7__.getUntracked;
valtio__WEBPACK_IMPORTED_MODULE_2__.trackMemo = proxy_compare__WEBPACK_IMPORTED_MODULE_7__.trackMemo;
valtio__WEBPACK_IMPORTED_MODULE_2__.bind = valtio_yjs__WEBPACK_IMPORTED_MODULE_4__.bind;
window.Y = yjs__WEBPACK_IMPORTED_MODULE_3__;
// TODO: should this be in the scope of loadApp?
const factories = {};
// standard factory decoder
(0,_cborDecoder__WEBPACK_IMPORTED_MODULE_1__.addExtension)({
    tag: 4000,
    Class: null,
    encode: null,
    decode([factoryName, closureArgs]) {
        return factories[factoryName](...closureArgs);
    },
});
// class decoder
(0,_cborDecoder__WEBPACK_IMPORTED_MODULE_1__.addExtension)({
    tag: 4001,
    Class: null,
    encode: null,
    decode([name, bases, non_methods, methods]) {
        // @ts-ignore
        const cls = Object.assign({}, non_methods);
        Object.defineProperties(cls, Object.fromEntries(Object.entries(methods).map(([key, fn]) => [
            key,
            {
                get: function () {
                    return _org_transcrypt_runtime___WEBPACK_IMPORTED_MODULE_6__.__get__(this, fn);
                },
                enumerable: true,
                configurable: true,
            },
        ])));
        return _org_transcrypt_runtime___WEBPACK_IMPORTED_MODULE_6__._class_(name, bases, cls);
    },
});
// __reduce__ decoder
(0,_cborDecoder__WEBPACK_IMPORTED_MODULE_1__.addExtension)({
    tag: 4002,
    Class: null,
    encode: null,
    decode([reconstructFn, args]) {
        return reconstructFn(...args);
    },
});
// instance decoder
(0,_cborDecoder__WEBPACK_IMPORTED_MODULE_1__.addExtension)({
    tag: 4003,
    Class: null,
    encode: null,
    decode([cls, dict]) {
        // @ts-ignore
        const instance = cls.__new__( /* should be called wipytth cls, TODO*/);
        // assign all properties from dict to instance
        for (const [key, value] of Object.entries(dict)) {
            instance[key] = value;
        }
        return instance;
    },
});
function makeLoadApp() {
    const cache = new Map();
    return function loadApp(serialized, marshalerId, chunkIdx) {
        if (!cache.has(marshalerId)) {
            let cached = [new _cborDecoder__WEBPACK_IMPORTED_MODULE_1__.Decoder({ useRecords: false, shareReferenceMap: true }), new Map(), 0];
            cache.set(marshalerId, cached);
        }
        let [decoder, chunkStore, lastOffset] = cache.get(marshalerId);
        if (chunkStore.has(chunkIdx)) {
            return chunkStore.get(chunkIdx);
        }
        const [cborDataB64, code] = serialized;
        Object.assign(factories, new Function(code)());
        const bytes = Uint8Array.from(atob(cborDataB64).slice(lastOffset), (c) => c.charCodeAt(0));
        const results = decoder.decodeMultiple(bytes);
        let nextIdx = chunkStore.size;
        for (const obj of results) {
            chunkStore.set(nextIdx++, obj);
        }
        cache.get(marshalerId)[2] += bytes.length;
        if (!chunkStore.has(chunkIdx)) {
            throw new RangeError(`Decoded ${chunkStore.size} objects, but chunkIdx ${chunkIdx} was not found.`);
        }
        return chunkStore.get(chunkIdx);
    };
}


/***/ }),

/***/ "./client/cborDecoder.js":
/*!*******************************!*\
  !*** ./client/cborDecoder.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Decoder: () => (/* binding */ Decoder),
/* harmony export */   addExtension: () => (/* binding */ addExtension)
/* harmony export */ });
/* unused harmony exports getPosition, checkedRead, read, isNativeAccelerationEnabled, setExtractor, Tag, typedArrays, clearSource, setSizeLimits, mult10, decode, decodeMultiple, FLOAT32_OPTIONS, roundFloat32 */
/**
 * Adapted from cbor-x to support sharing the referenceMap between
 * multiple decoding instances.
 * https://github.com/kriszyp/cbor-x/blob/master/decode.js
 */
let decoder;
try {
    decoder = new TextDecoder();
}
catch (error) { }
let src;
let srcEnd;
let position = 0;
let alreadySet;
const EMPTY_ARRAY = [];
const LEGACY_RECORD_INLINE_ID = 105;
const RECORD_DEFINITIONS_ID = 0xdffe;
const RECORD_INLINE_ID = 0xdfff; // temporary first-come first-serve tag // proposed tag: 0x7265 // 're'
const BUNDLED_STRINGS_ID = 0xdff9;
const PACKED_TABLE_TAG_ID = 51;
const PACKED_REFERENCE_TAG_ID = 6;
const STOP_CODE = {};
let maxArraySize = 112810000; // This is the maximum array size in V8. We would potentially detect and set it higher
// for JSC, but this is pretty large and should be sufficient for most use cases
let maxMapSize = 16810000; // JavaScript has a fixed maximum map size of about 16710000, but JS itself enforces this,
// so we don't need to
let maxObjectSize = 16710000; // This is the maximum number of keys in a Map. It takes over a minute to create this
// many keys in an object, so also probably a reasonable choice there.
let strings = EMPTY_ARRAY;
let stringPosition = 0;
let currentDecoder = {};
let currentStructures;
let srcString;
let srcStringStart = 0;
let srcStringEnd = 0;
let bundledStrings;
let referenceMap;
let currentExtensions = [];
let currentExtensionRanges = [];
let packedValues;
let dataView;
let restoreMapsAsObject;
let defaultOptions = {
    useRecords: false,
    mapsAsObjects: true
};
let sequentialMode = false;
let inlineObjectReadThreshold = 2;
var BlockedFunction; // we use search and replace to change the next call to BlockedFunction to avoid CSP issues for
// no-eval build
try {
    new Function('');
}
catch (error) {
    // if eval variants are not supported, do not create inline object readers ever
    inlineObjectReadThreshold = Infinity;
}
class Decoder {
    constructor(options) {
        if (options) {
            if ((options.keyMap || options._keyMap) && !options.useRecords) {
                options.useRecords = false;
                options.mapsAsObjects = true;
            }
            if (options.useRecords === false && options.mapsAsObjects === undefined)
                options.mapsAsObjects = true;
            if (options.getStructures)
                options.getShared = options.getStructures;
            if (options.getShared && !options.structures)
                (options.structures = []).uninitialized = true; // this is what we use to denote an uninitialized structures
            if (options.keyMap) {
                this.mapKey = new Map();
                for (let [k, v] of Object.entries(options.keyMap))
                    this.mapKey.set(v, k);
            }
        }
        Object.assign(this, options);
        if (this.shareReferenceMap) {
            this.referenceMap = new Map();
            this.referenceMap.id = 0;
        }
    }
    /*
    decodeKey(key) {
        return this.keyMap
            ? Object.keys(this.keyMap)[Object.values(this.keyMap).indexOf(key)] || key
            : key
    }
    */
    decodeKey(key) {
        return this.keyMap ? this.mapKey.get(key) || key : key;
    }
    encodeKey(key) {
        return this.keyMap && this.keyMap.hasOwnProperty(key) ? this.keyMap[key] : key;
    }
    encodeKeys(rec) {
        if (!this._keyMap)
            return rec;
        let map = new Map();
        for (let [k, v] of Object.entries(rec))
            map.set((this._keyMap.hasOwnProperty(k) ? this._keyMap[k] : k), v);
        return map;
    }
    decodeKeys(map) {
        if (!this._keyMap || map.constructor.name != 'Map')
            return map;
        if (!this._mapKey) {
            this._mapKey = new Map();
            for (let [k, v] of Object.entries(this._keyMap))
                this._mapKey.set(v, k);
        }
        let res = {};
        //map.forEach((v,k) => res[Object.keys(this._keyMap)[Object.values(this._keyMap).indexOf(k)] || k] = v)
        map.forEach((v, k) => res[safeKey(this._mapKey.has(k) ? this._mapKey.get(k) : k)] = v);
        return res;
    }
    mapDecode(source, end) {
        let res = this.decode(source);
        if (this._keyMap) {
            //Experiemntal support for Optimised KeyMap  decoding
            switch (res.constructor.name) {
                case 'Array': return res.map(r => this.decodeKeys(r));
                //case 'Map': return this.decodeKeys(res)
            }
        }
        return res;
    }
    decode(source, end) {
        if (this.shareReferenceMap) {
            referenceMap = this.referenceMap;
        }
        if (src) {
            // re-entrant execution, save the state and restore it after we do this decode
            return saveState(() => {
                clearSource();
                return this ? this.decode(source, end) : Decoder.prototype.decode.call(defaultOptions, source, end);
            });
        }
        srcEnd = end > -1 ? end : source.length;
        position = 0;
        stringPosition = 0;
        srcStringEnd = 0;
        srcString = null;
        strings = EMPTY_ARRAY;
        bundledStrings = null;
        src = source;
        // this provides cached access to the data view for a buffer if it is getting reused, which is a recommend
        // technique for getting data from a database where it can be copied into an existing buffer instead of creating
        // new ones
        try {
            dataView = source.dataView || (source.dataView = new DataView(source.buffer, source.byteOffset, source.byteLength));
        }
        catch (error) {
            // if it doesn't have a buffer, maybe it is the wrong type of object
            src = null;
            if (source instanceof Uint8Array)
                throw error;
            throw new Error('Source must be a Uint8Array or Buffer but was a ' + ((source && typeof source == 'object') ? source.constructor.name : typeof source));
        }
        if (this instanceof Decoder) {
            currentDecoder = this;
            packedValues = this.sharedValues &&
                (this.pack ? new Array(this.maxPrivatePackedValues || 16).concat(this.sharedValues) :
                    this.sharedValues);
            if (this.structures) {
                currentStructures = this.structures;
                return checkedRead(this);
            }
            else if (!currentStructures || currentStructures.length > 0) {
                currentStructures = [];
            }
        }
        else {
            currentDecoder = defaultOptions;
            if (!currentStructures || currentStructures.length > 0)
                currentStructures = [];
            packedValues = null;
        }
        return checkedRead(this);
    }
    decodeMultiple(source, forEach) {
        let values, lastPosition = 0;
        try {
            let size = source.length;
            sequentialMode = true;
            let value = this ? this.decode(source, size) : defaultDecoder.decode(source, size);
            if (forEach) {
                if (forEach(value) === false) {
                    return;
                }
                while (position < size) {
                    lastPosition = position;
                    if (forEach(checkedRead(this)) === false) {
                        return;
                    }
                }
            }
            else {
                values = [value];
                while (position < size) {
                    lastPosition = position;
                    values.push(checkedRead(this));
                }
                return values;
            }
        }
        catch (error) {
            error.lastPosition = lastPosition;
            error.values = values;
            throw error;
        }
        finally {
            sequentialMode = false;
            clearSource();
        }
    }
}
function getPosition() {
    return position;
}
function checkedRead(decoder) {
    try {
        let result = read();
        if (bundledStrings) {
            if (position >= bundledStrings.postBundlePosition) {
                let error = new Error('Unexpected bundle position');
                error.incomplete = true;
                throw error;
            }
            // bundled strings to skip past
            position = bundledStrings.postBundlePosition;
            bundledStrings = null;
        }
        if (position == srcEnd) {
            // finished reading this source, cleanup references
            currentStructures = null;
            src = null;
            if (referenceMap) {
                referenceMap = null;
            }
        }
        else if (position > srcEnd) {
            // over read
            let error = new Error('Unexpected end of CBOR data');
            error.incomplete = true;
            throw error;
        }
        else if (!sequentialMode) {
            throw new Error('Data read, but end of buffer not reached');
        }
        // else more to read, but we are reading sequentially, so don't clear source yet
        return result;
    }
    catch (error) {
        clearSource();
        if (error instanceof RangeError || error.message.startsWith('Unexpected end of buffer')) {
            error.incomplete = true;
        }
        throw error;
    }
}
function read() {
    let token = src[position++];
    let majorType = token >> 5;
    token = token & 0x1f;
    if (token > 0x17) {
        switch (token) {
            case 0x18:
                token = src[position++];
                break;
            case 0x19:
                if (majorType == 7) {
                    return getFloat16();
                }
                token = dataView.getUint16(position);
                position += 2;
                break;
            case 0x1a:
                if (majorType == 7) {
                    let value = dataView.getFloat32(position);
                    if (currentDecoder.useFloat32 > 2) {
                        // this does rounding of numbers that were encoded in 32-bit float to nearest significant decimal digit that could be preserved
                        let multiplier = mult10[((src[position] & 0x7f) << 1) | (src[position + 1] >> 7)];
                        position += 4;
                        return ((multiplier * value + (value > 0 ? 0.5 : -0.5)) >> 0) / multiplier;
                    }
                    position += 4;
                    return value;
                }
                token = dataView.getUint32(position);
                position += 4;
                break;
            case 0x1b:
                if (majorType == 7) {
                    let value = dataView.getFloat64(position);
                    position += 8;
                    return value;
                }
                if (majorType > 1) {
                    if (dataView.getUint32(position) > 0)
                        throw new Error('JavaScript does not support arrays, maps, or strings with length over 4294967295');
                    token = dataView.getUint32(position + 4);
                }
                else if (currentDecoder.int64AsNumber) {
                    token = dataView.getUint32(position) * 0x100000000;
                    token += dataView.getUint32(position + 4);
                }
                else
                    token = dataView.getBigUint64(position);
                position += 8;
                break;
            case 0x1f:
                // indefinite length
                switch (majorType) {
                    case 2: // byte string
                    case 3: // text string
                        throw new Error('Indefinite length not supported for byte or text strings');
                    case 4: // array
                        let array = [];
                        let value, i = 0;
                        while ((value = read()) != STOP_CODE) {
                            if (i >= maxArraySize)
                                throw new Error(`Array length exceeds ${maxArraySize}`);
                            array[i++] = value;
                        }
                        return majorType == 4 ? array : majorType == 3 ? array.join('') : Buffer.concat(array);
                    case 5: // map
                        let key;
                        if (currentDecoder.mapsAsObjects) {
                            let object = {};
                            let i = 0;
                            if (currentDecoder.keyMap) {
                                while ((key = read()) != STOP_CODE) {
                                    if (i++ >= maxMapSize)
                                        throw new Error(`Property count exceeds ${maxMapSize}`);
                                    object[safeKey(currentDecoder.decodeKey(key))] = read();
                                }
                            }
                            else {
                                while ((key = read()) != STOP_CODE) {
                                    if (i++ >= maxMapSize)
                                        throw new Error(`Property count exceeds ${maxMapSize}`);
                                    object[safeKey(key)] = read();
                                }
                            }
                            return object;
                        }
                        else {
                            if (restoreMapsAsObject) {
                                currentDecoder.mapsAsObjects = true;
                                restoreMapsAsObject = false;
                            }
                            let map = new Map();
                            if (currentDecoder.keyMap) {
                                let i = 0;
                                while ((key = read()) != STOP_CODE) {
                                    if (i++ >= maxMapSize) {
                                        throw new Error(`Map size exceeds ${maxMapSize}`);
                                    }
                                    map.set(currentDecoder.decodeKey(key), read());
                                }
                            }
                            else {
                                let i = 0;
                                while ((key = read()) != STOP_CODE) {
                                    if (i++ >= maxMapSize) {
                                        throw new Error(`Map size exceeds ${maxMapSize}`);
                                    }
                                    map.set(key, read());
                                }
                            }
                            return map;
                        }
                    case 7:
                        return STOP_CODE;
                    default:
                        throw new Error('Invalid major type for indefinite length ' + majorType);
                }
            default:
                throw new Error('Unknown token ' + token);
        }
    }
    switch (majorType) {
        case 0: // positive int
            return token;
        case 1: // negative int
            return ~token;
        case 2: // buffer
            return readBin(token);
        case 3: // string
            if (srcStringEnd >= position) {
                return srcString.slice(position - srcStringStart, (position += token) - srcStringStart);
            }
            if (srcStringEnd == 0 && srcEnd < 140 && token < 32) {
                // for small blocks, avoiding the overhead of the extract call is helpful
                let string = token < 16 ? shortStringInJS(token) : longStringInJS(token);
                if (string != null)
                    return string;
            }
            return readFixedString(token);
        case 4: // array
            if (token >= maxArraySize)
                throw new Error(`Array length exceeds ${maxArraySize}`);
            let array = new Array(token);
            //if (currentDecoder.keyMap) for (let i = 0; i < token; i++) array[i] = currentDecoder.decodeKey(read())
            //else
            for (let i = 0; i < token; i++)
                array[i] = read();
            return array;
        case 5: // map
            if (token >= maxMapSize)
                throw new Error(`Map size exceeds ${maxArraySize}`);
            if (currentDecoder.mapsAsObjects) {
                let object = {};
                if (currentDecoder.keyMap)
                    for (let i = 0; i < token; i++)
                        object[safeKey(currentDecoder.decodeKey(read()))] = read();
                else
                    for (let i = 0; i < token; i++)
                        object[safeKey(read())] = read();
                return object;
            }
            else {
                if (restoreMapsAsObject) {
                    currentDecoder.mapsAsObjects = true;
                    restoreMapsAsObject = false;
                }
                let map = new Map();
                if (currentDecoder.keyMap)
                    for (let i = 0; i < token; i++)
                        map.set(currentDecoder.decodeKey(read()), read());
                else
                    for (let i = 0; i < token; i++)
                        map.set(read(), read());
                return map;
            }
        case 6: // extension
            if (token >= BUNDLED_STRINGS_ID) {
                let structure = currentStructures[token & 0x1fff]; // check record structures first
                // At some point we may provide an option for dynamic tag assignment with a range like token >= 8 && (token < 16 || (token > 0x80 && token < 0xc0) || (token > 0x130 && token < 0x4000))
                if (structure) {
                    if (!structure.read)
                        structure.read = createStructureReader(structure);
                    return structure.read();
                }
                if (token < 0x10000) {
                    if (token == RECORD_INLINE_ID) { // we do a special check for this so that we can keep the
                        // currentExtensions as densely stored array (v8 stores arrays densely under about 3000 elements)
                        let length = readJustLength();
                        let id = read();
                        let structure = read();
                        recordDefinition(id, structure);
                        let object = {};
                        if (currentDecoder.keyMap)
                            for (let i = 2; i < length; i++) {
                                let key = currentDecoder.decodeKey(structure[i - 2]);
                                object[safeKey(key)] = read();
                            }
                        else
                            for (let i = 2; i < length; i++) {
                                let key = structure[i - 2];
                                object[safeKey(key)] = read();
                            }
                        return object;
                    }
                    else if (token == RECORD_DEFINITIONS_ID) {
                        let length = readJustLength();
                        let id = read();
                        for (let i = 2; i < length; i++) {
                            recordDefinition(id++, read());
                        }
                        return read();
                    }
                    else if (token == BUNDLED_STRINGS_ID) {
                        return readBundleExt();
                    }
                    if (currentDecoder.getShared) {
                        loadShared();
                        structure = currentStructures[token & 0x1fff];
                        if (structure) {
                            if (!structure.read)
                                structure.read = createStructureReader(structure);
                            return structure.read();
                        }
                    }
                }
            }
            let extension = currentExtensions[token];
            if (extension) {
                if (extension.handlesRead)
                    return extension(read);
                else
                    return extension(read());
            }
            else {
                let input = read();
                for (let i = 0; i < currentExtensionRanges.length; i++) {
                    let value = currentExtensionRanges[i](token, input);
                    if (value !== undefined)
                        return value;
                }
                return new Tag(input, token);
            }
        case 7: // fixed value
            switch (token) {
                case 0x14: return false;
                case 0x15: return true;
                case 0x16: return null;
                case 0x17: return; // undefined
                case 0x1f:
                default:
                    let packedValue = (packedValues || getPackedValues())[token];
                    if (packedValue !== undefined)
                        return packedValue;
                    throw new Error('Unknown token ' + token);
            }
        default: // negative int
            if (isNaN(token)) {
                let error = new Error('Unexpected end of CBOR data');
                error.incomplete = true;
                throw error;
            }
            throw new Error('Unknown CBOR token ' + token);
    }
}
const validName = /^[a-zA-Z_$][a-zA-Z\d_$]*$/;
function createStructureReader(structure) {
    if (!structure)
        throw new Error('Structure is required in record definition');
    function readObject() {
        // get the array size from the header
        let length = src[position++];
        //let majorType = token >> 5
        length = length & 0x1f;
        if (length > 0x17) {
            switch (length) {
                case 0x18:
                    length = src[position++];
                    break;
                case 0x19:
                    length = dataView.getUint16(position);
                    position += 2;
                    break;
                case 0x1a:
                    length = dataView.getUint32(position);
                    position += 4;
                    break;
                default:
                    throw new Error('Expected array header, but got ' + src[position - 1]);
            }
        }
        // This initial function is quick to instantiate, but runs slower. After several iterations pay the cost to build the faster function
        let compiledReader = this.compiledReader; // first look to see if we have the fast compiled function
        while (compiledReader) {
            // we have a fast compiled object literal reader
            if (compiledReader.propertyCount === length)
                return compiledReader(read); // with the right length, so we use it
            compiledReader = compiledReader.next; // see if there is another reader with the right length
        }
        if (this.slowReads++ >= inlineObjectReadThreshold) { // create a fast compiled reader
            let array = this.length == length ? this : this.slice(0, length);
            compiledReader = currentDecoder.keyMap
                ? new Function('r', 'return {' + array.map(k => currentDecoder.decodeKey(k)).map(k => validName.test(k) ? safeKey(k) + ':r()' : ('[' + JSON.stringify(k) + ']:r()')).join(',') + '}')
                : new Function('r', 'return {' + array.map(key => validName.test(key) ? safeKey(key) + ':r()' : ('[' + JSON.stringify(key) + ']:r()')).join(',') + '}');
            if (this.compiledReader)
                compiledReader.next = this.compiledReader; // if there is an existing one, we store multiple readers as a linked list because it is usually pretty rare to have multiple readers (of different length) for the same structure
            compiledReader.propertyCount = length;
            this.compiledReader = compiledReader;
            return compiledReader(read);
        }
        let object = {};
        if (currentDecoder.keyMap)
            for (let i = 0; i < length; i++)
                object[safeKey(currentDecoder.decodeKey(this[i]))] = read();
        else
            for (let i = 0; i < length; i++) {
                object[safeKey(this[i])] = read();
            }
        return object;
    }
    structure.slowReads = 0;
    return readObject;
}
function safeKey(key) {
    // protect against prototype pollution
    if (typeof key === 'string')
        return key === '__proto__' ? '__proto_' : key;
    if (typeof key === 'number' || typeof key === 'boolean' || typeof key === 'bigint')
        return key.toString();
    if (key == null)
        return key + '';
    // protect against expensive (DoS) string conversions
    throw new Error('Invalid property name type ' + typeof key);
}
let readFixedString = readStringJS;
let readString8 = readStringJS;
let readString16 = readStringJS;
let readString32 = readStringJS;
let isNativeAccelerationEnabled = false;
function setExtractor(extractStrings) {
    isNativeAccelerationEnabled = true;
    readFixedString = readString(1);
    readString8 = readString(2);
    readString16 = readString(3);
    readString32 = readString(5);
    function readString(headerLength) {
        return function readString(length) {
            let string = strings[stringPosition++];
            if (string == null) {
                if (bundledStrings)
                    return readStringJS(length);
                let extraction = extractStrings(position, srcEnd, length, src);
                if (typeof extraction == 'string') {
                    string = extraction;
                    strings = EMPTY_ARRAY;
                }
                else {
                    strings = extraction;
                    stringPosition = 1;
                    srcStringEnd = 1; // even if a utf-8 string was decoded, must indicate we are in the midst of extracted strings and can't skip strings
                    string = strings[0];
                    if (string === undefined)
                        throw new Error('Unexpected end of buffer');
                }
            }
            let srcStringLength = string.length;
            if (srcStringLength <= length) {
                position += length;
                return string;
            }
            srcString = string;
            srcStringStart = position;
            srcStringEnd = position + srcStringLength;
            position += length;
            return string.slice(0, length); // we know we just want the beginning
        };
    }
}
function readStringJS(length) {
    let result;
    if (length < 16) {
        if (result = shortStringInJS(length))
            return result;
    }
    if (length > 64 && decoder)
        return decoder.decode(src.subarray(position, position += length));
    const end = position + length;
    const units = [];
    result = '';
    while (position < end) {
        const byte1 = src[position++];
        if ((byte1 & 0x80) === 0) {
            // 1 byte
            units.push(byte1);
        }
        else if ((byte1 & 0xe0) === 0xc0) {
            // 2 bytes
            const byte2 = src[position++] & 0x3f;
            units.push(((byte1 & 0x1f) << 6) | byte2);
        }
        else if ((byte1 & 0xf0) === 0xe0) {
            // 3 bytes
            const byte2 = src[position++] & 0x3f;
            const byte3 = src[position++] & 0x3f;
            units.push(((byte1 & 0x1f) << 12) | (byte2 << 6) | byte3);
        }
        else if ((byte1 & 0xf8) === 0xf0) {
            // 4 bytes
            const byte2 = src[position++] & 0x3f;
            const byte3 = src[position++] & 0x3f;
            const byte4 = src[position++] & 0x3f;
            let unit = ((byte1 & 0x07) << 0x12) | (byte2 << 0x0c) | (byte3 << 0x06) | byte4;
            if (unit > 0xffff) {
                unit -= 0x10000;
                units.push(((unit >>> 10) & 0x3ff) | 0xd800);
                unit = 0xdc00 | (unit & 0x3ff);
            }
            units.push(unit);
        }
        else {
            units.push(byte1);
        }
        if (units.length >= 0x1000) {
            result += fromCharCode.apply(String, units);
            units.length = 0;
        }
    }
    if (units.length > 0) {
        result += fromCharCode.apply(String, units);
    }
    return result;
}
let fromCharCode = String.fromCharCode;
function longStringInJS(length) {
    let start = position;
    let bytes = new Array(length);
    for (let i = 0; i < length; i++) {
        const byte = src[position++];
        if ((byte & 0x80) > 0) {
            position = start;
            return;
        }
        bytes[i] = byte;
    }
    return fromCharCode.apply(String, bytes);
}
function shortStringInJS(length) {
    if (length < 4) {
        if (length < 2) {
            if (length === 0)
                return '';
            else {
                let a = src[position++];
                if ((a & 0x80) > 1) {
                    position -= 1;
                    return;
                }
                return fromCharCode(a);
            }
        }
        else {
            let a = src[position++];
            let b = src[position++];
            if ((a & 0x80) > 0 || (b & 0x80) > 0) {
                position -= 2;
                return;
            }
            if (length < 3)
                return fromCharCode(a, b);
            let c = src[position++];
            if ((c & 0x80) > 0) {
                position -= 3;
                return;
            }
            return fromCharCode(a, b, c);
        }
    }
    else {
        let a = src[position++];
        let b = src[position++];
        let c = src[position++];
        let d = src[position++];
        if ((a & 0x80) > 0 || (b & 0x80) > 0 || (c & 0x80) > 0 || (d & 0x80) > 0) {
            position -= 4;
            return;
        }
        if (length < 6) {
            if (length === 4)
                return fromCharCode(a, b, c, d);
            else {
                let e = src[position++];
                if ((e & 0x80) > 0) {
                    position -= 5;
                    return;
                }
                return fromCharCode(a, b, c, d, e);
            }
        }
        else if (length < 8) {
            let e = src[position++];
            let f = src[position++];
            if ((e & 0x80) > 0 || (f & 0x80) > 0) {
                position -= 6;
                return;
            }
            if (length < 7)
                return fromCharCode(a, b, c, d, e, f);
            let g = src[position++];
            if ((g & 0x80) > 0) {
                position -= 7;
                return;
            }
            return fromCharCode(a, b, c, d, e, f, g);
        }
        else {
            let e = src[position++];
            let f = src[position++];
            let g = src[position++];
            let h = src[position++];
            if ((e & 0x80) > 0 || (f & 0x80) > 0 || (g & 0x80) > 0 || (h & 0x80) > 0) {
                position -= 8;
                return;
            }
            if (length < 10) {
                if (length === 8)
                    return fromCharCode(a, b, c, d, e, f, g, h);
                else {
                    let i = src[position++];
                    if ((i & 0x80) > 0) {
                        position -= 9;
                        return;
                    }
                    return fromCharCode(a, b, c, d, e, f, g, h, i);
                }
            }
            else if (length < 12) {
                let i = src[position++];
                let j = src[position++];
                if ((i & 0x80) > 0 || (j & 0x80) > 0) {
                    position -= 10;
                    return;
                }
                if (length < 11)
                    return fromCharCode(a, b, c, d, e, f, g, h, i, j);
                let k = src[position++];
                if ((k & 0x80) > 0) {
                    position -= 11;
                    return;
                }
                return fromCharCode(a, b, c, d, e, f, g, h, i, j, k);
            }
            else {
                let i = src[position++];
                let j = src[position++];
                let k = src[position++];
                let l = src[position++];
                if ((i & 0x80) > 0 || (j & 0x80) > 0 || (k & 0x80) > 0 || (l & 0x80) > 0) {
                    position -= 12;
                    return;
                }
                if (length < 14) {
                    if (length === 12)
                        return fromCharCode(a, b, c, d, e, f, g, h, i, j, k, l);
                    else {
                        let m = src[position++];
                        if ((m & 0x80) > 0) {
                            position -= 13;
                            return;
                        }
                        return fromCharCode(a, b, c, d, e, f, g, h, i, j, k, l, m);
                    }
                }
                else {
                    let m = src[position++];
                    let n = src[position++];
                    if ((m & 0x80) > 0 || (n & 0x80) > 0) {
                        position -= 14;
                        return;
                    }
                    if (length < 15)
                        return fromCharCode(a, b, c, d, e, f, g, h, i, j, k, l, m, n);
                    let o = src[position++];
                    if ((o & 0x80) > 0) {
                        position -= 15;
                        return;
                    }
                    return fromCharCode(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o);
                }
            }
        }
    }
}
function readBin(length) {
    return currentDecoder.copyBuffers ?
        // specifically use the copying slice (not the node one)
        Uint8Array.prototype.slice.call(src, position, position += length) :
        src.subarray(position, position += length);
}
function readExt(length) {
    let type = src[position++];
    if (currentExtensions[type]) {
        return currentExtensions[type](src.subarray(position, position += length));
    }
    else
        throw new Error('Unknown extension type ' + type);
}
let f32Array = new Float32Array(1);
let u8Array = new Uint8Array(f32Array.buffer, 0, 4);
function getFloat16() {
    let byte0 = src[position++];
    let byte1 = src[position++];
    let exponent = (byte0 & 0x7f) >> 2;
    if (exponent === 0x1f) { // specials
        if (byte1 || (byte0 & 3))
            return NaN;
        return (byte0 & 0x80) ? -Infinity : Infinity;
    }
    if (exponent === 0) { // sub-normals
        // significand with 10 fractional bits and divided by 2^14
        let abs = (((byte0 & 3) << 8) | byte1) / (1 << 24);
        return (byte0 & 0x80) ? -abs : abs;
    }
    u8Array[3] = (byte0 & 0x80) | // sign bit
        ((exponent >> 1) + 56); // 4 of 5 of the exponent bits, re-offset-ed
    u8Array[2] = ((byte0 & 7) << 5) | // last exponent bit and first two mantissa bits
        (byte1 >> 3); // next 5 bits of mantissa
    u8Array[1] = byte1 << 5; // last three bits of mantissa
    u8Array[0] = 0;
    return f32Array[0];
}
let keyCache = new Array(4096);
function readKey() {
    let length = src[position++];
    if (length >= 0x60 && length < 0x78) {
        // fixstr, potentially use key cache
        length = length - 0x60;
        if (srcStringEnd >= position) // if it has been extracted, must use it (and faster anyway)
            return srcString.slice(position - srcStringStart, (position += length) - srcStringStart);
        else if (!(srcStringEnd == 0 && srcEnd < 180))
            return readFixedString(length);
    }
    else { // not cacheable, go back and do a standard read
        position--;
        return read();
    }
    let key = ((length << 5) ^ (length > 1 ? dataView.getUint16(position) : length > 0 ? src[position] : 0)) & 0xfff;
    let entry = keyCache[key];
    let checkPosition = position;
    let end = position + length - 3;
    let chunk;
    let i = 0;
    if (entry && entry.bytes == length) {
        while (checkPosition < end) {
            chunk = dataView.getUint32(checkPosition);
            if (chunk != entry[i++]) {
                checkPosition = 0x70000000;
                break;
            }
            checkPosition += 4;
        }
        end += 3;
        while (checkPosition < end) {
            chunk = src[checkPosition++];
            if (chunk != entry[i++]) {
                checkPosition = 0x70000000;
                break;
            }
        }
        if (checkPosition === end) {
            position = checkPosition;
            return entry.string;
        }
        end -= 3;
        checkPosition = position;
    }
    entry = [];
    keyCache[key] = entry;
    entry.bytes = length;
    while (checkPosition < end) {
        chunk = dataView.getUint32(checkPosition);
        entry.push(chunk);
        checkPosition += 4;
    }
    end += 3;
    while (checkPosition < end) {
        chunk = src[checkPosition++];
        entry.push(chunk);
    }
    // for small blocks, avoiding the overhead of the extract call is helpful
    let string = length < 16 ? shortStringInJS(length) : longStringInJS(length);
    if (string != null)
        return entry.string = string;
    return entry.string = readFixedString(length);
}
class Tag {
    constructor(value, tag) {
        this.value = value;
        this.tag = tag;
    }
}
currentExtensions[0] = (dateString) => {
    // string date extension
    return new Date(dateString);
};
currentExtensions[1] = (epochSec) => {
    // numeric date extension
    return new Date(Math.round(epochSec * 1000));
};
currentExtensions[2] = (buffer) => {
    // bigint extension
    let value = BigInt(0);
    for (let i = 0, l = buffer.byteLength; i < l; i++) {
        value = BigInt(buffer[i]) + (value << BigInt(8));
    }
    return value;
};
currentExtensions[3] = (buffer) => {
    // negative bigint extension
    return BigInt(-1) - currentExtensions[2](buffer);
};
currentExtensions[4] = (fraction) => {
    // best to reparse to maintain accuracy
    return +(fraction[1] + 'e' + fraction[0]);
};
currentExtensions[5] = (fraction) => {
    // probably not sufficiently accurate
    return fraction[1] * Math.exp(fraction[0] * Math.log(2));
};
// the registration of the record definition extension
const recordDefinition = (id, structure) => {
    id = id - 0xe000;
    let existingStructure = currentStructures[id];
    if (existingStructure && existingStructure.isShared) {
        (currentStructures.restoreStructures || (currentStructures.restoreStructures = []))[id] = existingStructure;
    }
    currentStructures[id] = structure;
    structure.read = createStructureReader(structure);
};
currentExtensions[LEGACY_RECORD_INLINE_ID] = (data) => {
    let length = data.length;
    let structure = data[1];
    recordDefinition(data[0], structure);
    let object = {};
    for (let i = 2; i < length; i++) {
        let key = structure[i - 2];
        object[safeKey(key)] = data[i];
    }
    return object;
};
currentExtensions[14] = (value) => {
    if (bundledStrings)
        return bundledStrings[0].slice(bundledStrings.position0, bundledStrings.position0 += value);
    return new Tag(value, 14);
};
currentExtensions[15] = (value) => {
    if (bundledStrings)
        return bundledStrings[1].slice(bundledStrings.position1, bundledStrings.position1 += value);
    return new Tag(value, 15);
};
let glbl = { Error, RegExp };
currentExtensions[27] = (data) => {
    return (glbl[data[0]] || Error)(data[1], data[2]);
};
const packedTable = (read) => {
    if (src[position++] != 0x84) {
        let error = new Error('Packed values structure must be followed by a 4 element array');
        if (src.length < position)
            error.incomplete = true;
        throw error;
    }
    let newPackedValues = read(); // packed values
    if (!newPackedValues || !newPackedValues.length) {
        let error = new Error('Packed values structure must be followed by a 4 element array');
        error.incomplete = true;
        throw error;
    }
    packedValues = packedValues ? newPackedValues.concat(packedValues.slice(newPackedValues.length)) : newPackedValues;
    packedValues.prefixes = read();
    packedValues.suffixes = read();
    return read(); // read the rump
};
packedTable.handlesRead = true;
currentExtensions[51] = packedTable;
currentExtensions[PACKED_REFERENCE_TAG_ID] = (data) => {
    if (!packedValues) {
        if (currentDecoder.getShared)
            loadShared();
        else
            return new Tag(data, PACKED_REFERENCE_TAG_ID);
    }
    if (typeof data == 'number')
        return packedValues[16 + (data >= 0 ? 2 * data : (-2 * data - 1))];
    let error = new Error('No support for non-integer packed references yet');
    if (data === undefined)
        error.incomplete = true;
    throw error;
};
// The following code is an incomplete implementation of http://cbor.schmorp.de/stringref
// the real thing would need to implemennt more logic to populate the stringRefs table and
// maintain a stack of stringRef "namespaces".
//
// currentExtensions[25] = (id) => {
// 	return stringRefs[id]
// }
// currentExtensions[256] = (read) => {
// 	stringRefs = []
// 	try {
// 		return read()
// 	} finally {
// 		stringRefs = null
// 	}
// }
// currentExtensions[256].handlesRead = true
currentExtensions[28] = (read) => {
    // shareable http://cbor.schmorp.de/value-sharing (for structured clones)
    if (!referenceMap) {
        referenceMap = new Map();
        referenceMap.id = 0;
    }
    let id = referenceMap.id++;
    let startingPosition = position;
    let token = src[position];
    let target;
    // TODO: handle Maps, Sets, and other types that can cycle; this is complicated, because you potentially need to read
    // ahead past references to record structure definitions
    if ((token >> 5) == 4)
        target = [];
    else
        target = {};
    let refEntry = { target }; // a placeholder object
    referenceMap.set(id, refEntry);
    let targetProperties = read(); // read the next value as the target object to id
    if (refEntry.used) { // there is a cycle, so we have to assign properties to original target
        if (Object.getPrototypeOf(target) !== Object.getPrototypeOf(targetProperties)) {
            // this means that the returned target does not match the targetProperties, so we need rerun the read to
            // have the correctly create instance be assigned as a reference, then we do the copy the properties back to the
            // target
            // reset the position so that the read can be repeated
            position = startingPosition;
            // the returned instance is our new target for references
            target = targetProperties;
            referenceMap.set(id, { target });
            targetProperties = read();
        }
        return Object.assign(target, targetProperties);
    }
    refEntry.target = targetProperties; // the placeholder wasn't used, replace with the deserialized one
    return targetProperties; // no cycle, can just use the returned read object
};
currentExtensions[28].handlesRead = true;
currentExtensions[29] = (id) => {
    // sharedref http://cbor.schmorp.de/value-sharing (for structured clones)
    let refEntry = referenceMap.get(id);
    refEntry.used = true;
    return refEntry.target;
};
currentExtensions[258] = (array) => new Set(array); // https://github.com/input-output-hk/cbor-sets-spec/blob/master/CBOR_SETS.md
(currentExtensions[259] = (read) => {
    // https://github.com/shanewholloway/js-cbor-codec/blob/master/docs/CBOR-259-spec
    // for decoding as a standard Map
    if (currentDecoder.mapsAsObjects) {
        currentDecoder.mapsAsObjects = false;
        restoreMapsAsObject = true;
    }
    return read();
}).handlesRead = true;
function combine(a, b) {
    if (typeof a === 'string')
        return a + b;
    if (a instanceof Array)
        return a.concat(b);
    return Object.assign({}, a, b);
}
function getPackedValues() {
    if (!packedValues) {
        if (currentDecoder.getShared)
            loadShared();
        else
            throw new Error('No packed values available');
    }
    return packedValues;
}
const SHARED_DATA_TAG_ID = 0x53687264; // ascii 'Shrd'
currentExtensionRanges.push((tag, input) => {
    if (tag >= 225 && tag <= 255)
        return combine(getPackedValues().prefixes[tag - 224], input);
    if (tag >= 28704 && tag <= 32767)
        return combine(getPackedValues().prefixes[tag - 28672], input);
    if (tag >= 1879052288 && tag <= 2147483647)
        return combine(getPackedValues().prefixes[tag - 1879048192], input);
    if (tag >= 216 && tag <= 223)
        return combine(input, getPackedValues().suffixes[tag - 216]);
    if (tag >= 27647 && tag <= 28671)
        return combine(input, getPackedValues().suffixes[tag - 27639]);
    if (tag >= 1811940352 && tag <= 1879048191)
        return combine(input, getPackedValues().suffixes[tag - 1811939328]);
    if (tag == SHARED_DATA_TAG_ID) { // we do a special check for this so that we can keep the currentExtensions as densely stored array (v8 stores arrays densely under about 3000 elements)
        return {
            packedValues: packedValues,
            structures: currentStructures.slice(0),
            version: input,
        };
    }
    if (tag == 55799) // self-descriptive CBOR tag, just return input value
        return input;
});
const isLittleEndianMachine = new Uint8Array(new Uint16Array([1]).buffer)[0] == 1;
const typedArrays = [Uint8Array, Uint8ClampedArray, Uint16Array, Uint32Array,
    typeof BigUint64Array == 'undefined' ? { name: 'BigUint64Array' } : BigUint64Array, Int8Array, Int16Array, Int32Array,
    typeof BigInt64Array == 'undefined' ? { name: 'BigInt64Array' } : BigInt64Array, Float32Array, Float64Array];
const typedArrayTags = [64, 68, 69, 70, 71, 72, 77, 78, 79, 85, 86];
for (let i = 0; i < typedArrays.length; i++) {
    registerTypedArray(typedArrays[i], typedArrayTags[i]);
}
function registerTypedArray(TypedArray, tag) {
    let dvMethod = 'get' + TypedArray.name.slice(0, -5);
    let bytesPerElement;
    if (typeof TypedArray === 'function')
        bytesPerElement = TypedArray.BYTES_PER_ELEMENT;
    else
        TypedArray = null;
    for (let littleEndian = 0; littleEndian < 2; littleEndian++) {
        if (!littleEndian && bytesPerElement == 1)
            continue;
        let sizeShift = bytesPerElement == 2 ? 1 : bytesPerElement == 4 ? 2 : bytesPerElement == 8 ? 3 : 0;
        currentExtensions[littleEndian ? tag : (tag - 4)] = (bytesPerElement == 1 || littleEndian == isLittleEndianMachine) ? (buffer) => {
            if (!TypedArray)
                throw new Error('Could not find typed array for code ' + tag);
            if (!currentDecoder.copyBuffers) {
                // try provide a direct view, but will only work if we are byte-aligned
                if (bytesPerElement === 1 ||
                    bytesPerElement === 2 && !(buffer.byteOffset & 1) ||
                    bytesPerElement === 4 && !(buffer.byteOffset & 3) ||
                    bytesPerElement === 8 && !(buffer.byteOffset & 7))
                    return new TypedArray(buffer.buffer, buffer.byteOffset, buffer.byteLength >> sizeShift);
            }
            // we have to slice/copy here to get a new ArrayBuffer, if we are not word/byte aligned
            return new TypedArray(Uint8Array.prototype.slice.call(buffer, 0).buffer);
        } : buffer => {
            if (!TypedArray)
                throw new Error('Could not find typed array for code ' + tag);
            let dv = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
            let elements = buffer.length >> sizeShift;
            let ta = new TypedArray(elements);
            let method = dv[dvMethod];
            for (let i = 0; i < elements; i++) {
                ta[i] = method.call(dv, i << sizeShift, littleEndian);
            }
            return ta;
        };
    }
}
function readBundleExt() {
    let length = readJustLength();
    let bundlePosition = position + read();
    for (let i = 2; i < length; i++) {
        // skip past bundles that were already read
        let bundleLength = readJustLength(); // this will increment position, so must add to position afterwards
        position += bundleLength;
    }
    let dataPosition = position;
    position = bundlePosition;
    bundledStrings = [readStringJS(readJustLength()), readStringJS(readJustLength())];
    bundledStrings.position0 = 0;
    bundledStrings.position1 = 0;
    bundledStrings.postBundlePosition = position;
    position = dataPosition;
    return read();
}
function readJustLength() {
    let token = src[position++] & 0x1f;
    if (token > 0x17) {
        switch (token) {
            case 0x18:
                token = src[position++];
                break;
            case 0x19:
                token = dataView.getUint16(position);
                position += 2;
                break;
            case 0x1a:
                token = dataView.getUint32(position);
                position += 4;
                break;
        }
    }
    return token;
}
function loadShared() {
    if (currentDecoder.getShared) {
        let sharedData = saveState(() => {
            // save the state in case getShared modifies our buffer
            src = null;
            return currentDecoder.getShared();
        }) || {};
        let updatedStructures = sharedData.structures || [];
        currentDecoder.sharedVersion = sharedData.version;
        packedValues = currentDecoder.sharedValues = sharedData.packedValues;
        if (currentStructures === true)
            currentDecoder.structures = currentStructures = updatedStructures;
        else
            currentStructures.splice.apply(currentStructures, [0, updatedStructures.length].concat(updatedStructures));
    }
}
function saveState(callback) {
    let savedSrcEnd = srcEnd;
    let savedPosition = position;
    let savedStringPosition = stringPosition;
    let savedSrcStringStart = srcStringStart;
    let savedSrcStringEnd = srcStringEnd;
    let savedSrcString = srcString;
    let savedStrings = strings;
    let savedReferenceMap = referenceMap;
    let savedBundledStrings = bundledStrings;
    // TODO: We may need to revisit this if we do more external calls to user code (since it could be slow)
    let savedSrc = new Uint8Array(src.slice(0, srcEnd)); // we copy the data in case it changes while external data is processed
    let savedStructures = currentStructures;
    let savedDecoder = currentDecoder;
    let savedSequentialMode = sequentialMode;
    let value = callback();
    srcEnd = savedSrcEnd;
    position = savedPosition;
    stringPosition = savedStringPosition;
    srcStringStart = savedSrcStringStart;
    srcStringEnd = savedSrcStringEnd;
    srcString = savedSrcString;
    strings = savedStrings;
    referenceMap = savedReferenceMap;
    bundledStrings = savedBundledStrings;
    src = savedSrc;
    sequentialMode = savedSequentialMode;
    currentStructures = savedStructures;
    currentDecoder = savedDecoder;
    dataView = new DataView(src.buffer, src.byteOffset, src.byteLength);
    return value;
}
function clearSource() {
    src = null;
    referenceMap = null;
    currentStructures = null;
}
function addExtension(extension) {
    currentExtensions[extension.tag] = extension.decode;
}
function setSizeLimits(limits) {
    if (limits.maxMapSize)
        maxMapSize = limits.maxMapSize;
    if (limits.maxArraySize)
        maxArraySize = limits.maxArraySize;
    if (limits.maxObjectSize)
        maxObjectSize = limits.maxObjectSize;
}
const mult10 = new Array(147); // this is a table matching binary exponents to the multiplier to determine significant digit rounding
for (let i = 0; i < 256; i++) {
    mult10[i] = +('1e' + Math.floor(45.15 - i * 0.30103));
}
let defaultDecoder = new Decoder({ useRecords: false });
const decode = defaultDecoder.decode;
const decodeMultiple = defaultDecoder.decodeMultiple;
const FLOAT32_OPTIONS = {
    NEVER: 0,
    ALWAYS: 1,
    DECIMAL_ROUND: 3,
    DECIMAL_FIT: 4
};
function roundFloat32(float32Number) {
    f32Array[0] = float32Number;
    let multiplier = mult10[((u8Array[3] & 0x7f) << 1) | (u8Array[2] >> 7)];
    return ((multiplier * float32Number + (float32Number > 0 ? 0.5 : -0.5)) >> 0) / multiplier;
}


/***/ }),

/***/ "./client/components/Loading/index.tsx":
/*!*********************************************!*\
  !*** ./client/components/Loading/index.tsx ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
/* harmony import */ var _style_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./style.css */ "./client/components/Loading/style.css");


/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (() => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("div", { style: { 'minHeight': '80px', 'minWidth': '80px' }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("div", { className: "loading", style: {
            'position': 'absolute',
            'top': '50%',
            'left': '50%',
            'transform': 'translateX(-50%) translateY(-50%)',
            'textAlign': 'center',
        }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("svg", { width: "38", height: "38", viewBox: "0 0 38 38", xmlns: "http://www.w3.org/2000/svg", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("defs", { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("linearGradient", { x1: "8.042%", y1: "0%", x2: "65.682%", y2: "23.865%", id: "a", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("stop", { stopOpacity: "0", offset: "0%" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("stop", { stopOpacity: ".631", offset: "63.146%" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("stop", { offset: "100%" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("g", { fill: "none", fillRule: "evenodd", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("g", { transform: "translate(1 1)", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", { d: "M36 18c0-9.94-8.06-18-18-18", id: "Oval-2", stroke: "url(#a)", strokeWidth: "2", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("animateTransform", { attributeName: "transform", type: "rotate", from: "0 18 18", to: "360 18 18", dur: "0.9s", repeatCount: "indefinite" }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("circle", { cx: "36", cy: "18", r: "1", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("animateTransform", { attributeName: "transform", type: "rotate", from: "0 18 18", to: "360 18 18", dur: "0.9s", repeatCount: "indefinite" }) })] }) })] }) }) })));


/***/ }),

/***/ "./client/components/Loading/style.css":
/*!*********************************************!*\
  !*** ./client/components/Loading/style.css ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __unused_webpack___webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./client/components/Loading/style.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* unused harmony default export */ var __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./client/globals.ts":
/*!***************************!*\
  !*** ./client/globals.ts ***!
  \***************************/
/***/ (() => {



/***/ }),

/***/ "./client/jupyter/keep-hidden-cell-output.ts":
/*!***************************************************!*\
  !*** ./client/jupyter/keep-hidden-cell-output.ts ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __unused_webpack___webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* -----------------------------------------------------------------------------
| Modified by PW from the JupyterLab repository with an ugly monkey patch hack
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
//@ts-ignore

//@ts-ignore

/**
 * The namespace for the `CodeCell` class statics.
 */
/**
 * Execute a cell given a client session.
 */
(function (CodeCell) {
    function execute(cell, sessionContext, metadata) {
        return __awaiter(this, void 0, void 0, function* () {
            var _a, _b, _c, _d, _e, _f;
            const model /* ICodeCellModel */ = cell.model;
            const code = model.sharedModel
                ? model.sharedModel.getSource()
                : model.value.text;
            const canChangeHiddenState = !((_e = (_d = (_c = (_b = (_a = cell === null || cell === void 0 ? void 0 : cell.outputArea) === null || _a === void 0 ? void 0 : _a.widgets) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c.widgets) === null || _d === void 0 ? void 0 : _d[1]) === null || _e === void 0 ? void 0 : _e.keepHiddenWhenExecuted);
            // ^--- modified here
            if (!code.trim() || !((_f = sessionContext.session) === null || _f === void 0 ? void 0 : _f.kernel)) {
                if (model.sharedModel) {
                    model.sharedModel.transact(() => {
                        model.clearExecution();
                    }, false, "silent-change");
                }
                else {
                    model.clearExecution();
                }
                return;
            }
            const cellId = {
                cellId: model.sharedModel ? model.sharedModel.getId() : model.id,
            };
            metadata = Object.assign(Object.assign(Object.assign({}, (model.metadata.toJSON ? model.metadata.toJSON() : model.metadata)), metadata), cellId);
            const { recordTiming } = metadata;
            if (model.sharedModel) {
                model.sharedModel.transact(() => {
                    model.clearExecution();
                    if (canChangeHiddenState) {
                        cell.outputHidden = false;
                    }
                }, false, "silent-change");
            }
            else {
                model.clearExecution();
                // modified here: wrapped in a if statement here
                if (canChangeHiddenState) {
                    cell.outputHidden = false;
                }
            }
            if (cell.setPrompt) {
                cell.setPrompt("*");
            }
            else {
                model.executionState = "running";
            }
            model.trusted = true;
            let future;
            try {
                const msgPromise = _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputArea.execute(code, cell.outputArea, sessionContext, metadata);
                // cell.outputArea.future assigned synchronously in `execute`
                if (recordTiming) {
                    const recordTimingHook = (msg) => {
                        let label;
                        switch (msg.header.msg_type) {
                            case "status":
                                label = `status.${msg.content.execution_state}`;
                                break;
                            case "execute_input":
                                label = "execute_input";
                                break;
                            default:
                                return true;
                        }
                        // If the data is missing, estimate it to now
                        // Date was added in 5.1: https://jupyter-client.readthedocs.io/en/stable/messaging.html#message-header
                        const value = msg.header.date || new Date().toISOString();
                        const timingInfo = Object.assign({}, model.getMetadata
                            ? model.getMetadata("execution")
                            : model.metadata.get("execution"));
                        timingInfo[`iopub.${label}`] = value;
                        model.setMetadata
                            ? model.setMetadata("execution", timingInfo)
                            : model.metadata.set("execution", timingInfo);
                        return true;
                    };
                    cell.outputArea.future.registerMessageHook(recordTimingHook);
                }
                else {
                    model.deleteMetadata
                        ? model.deleteMetadata("execution")
                        : model.metadata.delete("execution");
                }
                // Save this execution's future so we can compare in the catch below.
                future = cell.outputArea.future;
                const msg = (yield msgPromise);
                model.executionCount = msg.content.execution_count;
                if (recordTiming) {
                    const timingInfo = Object.assign({}, model.getMetadata
                        ? model.getMetadata("execution")
                        : model.metadata.get("execution"));
                    const started = msg.metadata.started;
                    // Started is not in the API, but metadata IPyKernel sends
                    if (started) {
                        timingInfo["shell.execute_reply.started"] = started;
                    }
                    // Per above, the 5.0 spec does not assume date, so we estimate is required
                    const finished = msg.header.date;
                    timingInfo["shell.execute_reply"] =
                        finished || new Date().toISOString();
                    model.setMetadata
                        ? model.setMetadata("execution", timingInfo)
                        : model.metadata.set("execution", timingInfo);
                    if (canChangeHiddenState) {
                        // <--- modified here
                        cell.outputHidden = false;
                    } // <--- modified here
                }
                return msg;
            }
            catch (e) {
                // If we started executing, and the cell is still indicating this
                // execution, clear the prompt.
                if (future && !cell.isDisposed && cell.outputArea.future === future) {
                    if (cell.setPrompt) {
                        cell.setPrompt("");
                    }
                    else {
                        model.executionState = "idle";
                    }
                    if (recordTiming && future.isDisposed) {
                        // Record the time when the cell execution was aborted
                        const timingInfo = Object.assign({}, model.getMetadata
                            ? model.getMetadata("execution")
                            : model.metadata.get("execution"));
                        timingInfo["execution_failed"] = new Date().toISOString();
                        model.setMetadata
                            ? model.setMetadata("execution", timingInfo)
                            : model.metadata.set("execution", timingInfo);
                    }
                }
                throw e;
            }
        });
    }
    // @ts-ignore
    CodeCell.old_execute = CodeCell.execute;
    CodeCell.execute = execute;
})(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell);


/***/ }),

/***/ "./client/jupyter/manager.ts":
/*!***********************************!*\
  !*** ./client/jupyter/manager.ts ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ PretJupyterHandler)
/* harmony export */ });
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var use_sync_external_store_shim__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! use-sync-external-store/shim */ "./node_modules/use-sync-external-store/shim/index.js");
/* harmony import */ var _appLoader__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../appLoader */ "./client/appLoader.ts");
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};



// @ts-ignore
(react__WEBPACK_IMPORTED_MODULE_1___default().useSyncExternalStore) = use_sync_external_store_shim__WEBPACK_IMPORTED_MODULE_2__.useSyncExternalStore;

class PretJupyterHandler {
    get readyResolve() {
        return this._readyResolve;
    }
    set readyResolve(value) {
        this._readyResolve = value;
    }
    constructor(context, settings) {
        var _a, _b;
        this.sendMessage = (method, data) => {
            this.comm.send({
                'method': method,
                'data': data
            });
        };
        this.handleCommOpen = (comm, msg) => {
            console.info("Comm is open", comm.commId);
            this.comm = comm;
            this.comm.onMsg = this.handleCommMessage;
            this._readyResolve();
        };
        /**
         * Get the currently-registered comms.
         */
        this.getCommInfo = () => __awaiter(this, void 0, void 0, function* () {
            var _a, _b;
            let kernel = (_b = (_a = this.context) === null || _a === void 0 ? void 0 : _a.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
            if (!kernel) {
                throw new Error('No current kernel');
            }
            const reply = yield kernel.requestCommInfo({ target_name: this.commTargetName });
            if (reply.content.status === 'ok') {
                return (reply.content).comms;
            }
            else {
                return {};
            }
        });
        this.connectToAnyKernel = () => __awaiter(this, void 0, void 0, function* () {
            var _a, _b, _c, _d, _e, _f;
            if (!((_a = this.context) === null || _a === void 0 ? void 0 : _a.sessionContext)) {
                console.warn("No session context");
                return;
            }
            console.info("Awaiting session to be ready");
            yield this.context.sessionContext.ready;
            if (((_b = this.context) === null || _b === void 0 ? void 0 : _b.sessionContext.session.kernel.handleComms) === false) {
                console.warn("Comms are disabled");
                return;
            }
            const allCommIds = yield this.getCommInfo();
            const relevantCommIds = Object.keys(allCommIds).filter(key => allCommIds[key]['target_name'] === this.commTargetName);
            console.info("Jupyter annotator comm ids", relevantCommIds, "(there should be at most one)");
            if (relevantCommIds.length === 0) {
                const comm = (_d = (_c = this.context) === null || _c === void 0 ? void 0 : _c.sessionContext.session) === null || _d === void 0 ? void 0 : _d.kernel.createComm(this.commTargetName);
                comm.open();
                this.handleCommOpen(comm);
            }
            else if (relevantCommIds.length >= 1) {
                if (relevantCommIds.length > 1) {
                    console.warn("Multiple comms found for target name", this.commTargetName, "using the first one");
                }
                const comm = (_f = (_e = this.context) === null || _e === void 0 ? void 0 : _e.sessionContext.session) === null || _f === void 0 ? void 0 : _f.kernel.createComm(this.commTargetName, relevantCommIds[0]);
                // comm.open()
                this.handleCommOpen(comm);
            }
        });
        this.handleCommMessage = (msg) => {
            try {
                const { method, data } = msg.content.data;
                this.appManager.handle_message(method, data);
            }
            catch (e) {
                console.error("Error during comm message reception", e);
            }
        };
        /**
         * Register a new kernel
         */
        this.handleKernelChanged = ({ name, oldValue, newValue }) => {
            console.info("handleKernelChanged", oldValue, newValue);
            if (oldValue) {
                this.comm = null;
                oldValue.removeCommTarget(this.commTargetName, this.handleCommOpen);
            }
            if (newValue) {
                newValue.registerCommTarget(this.commTargetName, this.handleCommOpen);
            }
        };
        this.handleKernelStatusChange = (status) => {
            switch (status) {
                case 'autorestarting':
                case 'restarting':
                case 'dead':
                    //this.disconnect();
                    break;
                default:
            }
        };
        this.commTargetName = 'pret';
        this.context = context;
        this.comm = null;
        this.unpack = (0,_appLoader__WEBPACK_IMPORTED_MODULE_3__.makeLoadApp)();
        this.appManager = null;
        this.ready = new Promise((resolve, reject) => {
            this._readyResolve = resolve;
            this._readyReject = reject;
        });
        // https://github.com/jupyter-widgets/ipywidgets/commit/5b922f23e54f3906ed9578747474176396203238
        context === null || context === void 0 ? void 0 : context.sessionContext.kernelChanged.connect((sender, args) => {
            this.handleKernelChanged(args);
        });
        context === null || context === void 0 ? void 0 : context.sessionContext.statusChanged.connect((sender, status) => {
            this.handleKernelStatusChange(status);
        });
        if ((_a = context === null || context === void 0 ? void 0 : context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) {
            this.handleKernelChanged({
                name: 'kernel',
                oldValue: null,
                newValue: (_b = context.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel
            });
        }
        this.connectToAnyKernel().then();
        this.settings = settings;
    }
    /**
     * Deserialize a view data to turn it into a callable js function
     * @param view_data
     */
    unpackView({ serialized, marshaler_id, chunk_idx }) {
        const [renderable, manager] = this.unpack(serialized, marshaler_id, chunk_idx);
        this.appManager = manager;
        this.appManager.register_environment_handler(this);
        return renderable;
    }
}


/***/ }),

/***/ "./client/jupyter/plugin.tsx":
/*!***********************************!*\
  !*** ./client/jupyter/plugin.tsx ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PretClonedArea: () => (/* binding */ PretClonedArea),
/* harmony export */   contextToPretJupyterHandlerRegistry: () => (/* binding */ contextToPretJupyterHandlerRegistry),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   registerOutputListener: () => (/* binding */ registerOutputListener),
/* harmony export */   registerPretJupyterHandler: () => (/* binding */ registerPretJupyterHandler)
/* harmony export */ });
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole");
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./manager */ "./client/jupyter/manager.ts");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./widget */ "./client/jupyter/widget.tsx");
/* harmony import */ var _keep_hidden_cell_output__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./keep-hidden-cell-output */ "./client/jupyter/keep-hidden-cell-output.ts");
/* harmony import */ var _style_css__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./style.css */ "./client/jupyter/style.css");
/* harmony import */ var _pret_globals__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @pret-globals */ "./client/globals.ts");
/* harmony import */ var _pret_globals__WEBPACK_IMPORTED_MODULE_19___default = /*#__PURE__*/__webpack_require__.n(_pret_globals__WEBPACK_IMPORTED_MODULE_19__);
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};

 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */
// import {LabIcon} from '@jupyterlab/ui-components'; /* @ts-ignore */
 /* @ts-ignore */
 /* @ts-ignore */





const MIMETYPE = 'application/vnd.pret+json';
// // export const notebookIcon = new LabIcon({name: 'ui-components:pret', svgstr: pretSvgstr});
const contextToPretJupyterHandlerRegistry = new _lumino_properties__WEBPACK_IMPORTED_MODULE_2__.AttachedProperty({
    name: 'widgetManager',
    create: () => undefined
});
const SETTINGS = { saveState: false };
/**
 * Iterate through all pret renderers in a notebook.
 */
function* getWidgetsFromNotebook(notebook) {
    // @ts-ignore
    for (const cell of notebook.widgets) {
        if (cell.model.type === 'code') {
            // @ts-ignore
            for (const codecell of cell.outputArea.widgets) {
                for (const output of (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.toArray)(codecell.children())) {
                    if (output instanceof _widget__WEBPACK_IMPORTED_MODULE_16__.PretViewWidget) {
                        yield output;
                    }
                }
            }
        }
    }
}
function* chain(...args) {
    for (const it of args) {
        yield* it;
    }
}
/**
 * Iterate through all matching linked output views
 */
function* getLinkedWidgetsFromApp(jupyterApp, path) {
    const linkedViews = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.filter)(Array.from(jupyterApp.shell.widgets("main")), 
    // @ts-ignore
    (w) => w.id.startsWith('LinkedOutputView-') && w.path === path);
    for (const view of (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.toArray)(linkedViews)) {
        for (const outputs of view.children()) {
            for (const output of outputs.children()) {
                // TODO: do we need instanceof ?
                if (output instanceof _widget__WEBPACK_IMPORTED_MODULE_16__.PretViewWidget) {
                    yield output;
                }
            }
        }
    }
}
/**
 * A widget hosting a cloned output area.
 */
class PretClonedArea extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_13__.Panel {
    constructor(options) {
        super();
        this._cell = null;
        this._notebook = options.notebook;
        this._index = options.index !== undefined ? options.index : -1;
        this._cell = options.cell || null;
        this.id = `PretArea-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_14__.UUID.uuid4()}`;
        // this.title.icon = notebookIcon;
        this.title.caption = this._notebook.title.label ? `For Notebook: ${this._notebook.title.label || ''}` : '';
        this.addClass('jp-LinkedOutputView');
        // Wait for the notebook to be loaded before
        // cloning the output area.
        void this._notebook.context.ready.then(() => {
            if (!this._cell) {
                this._cell = this._notebook.content.widgets[this._index];
            }
            if (!this._cell || this._cell.model.type !== 'code') {
                this.dispose();
                return;
            }
            // @ts-ignore
            // const widget = this._cell.outputArea.widgets?.[0]?.widgets?.[1] as PretWidget;
            // TODO title label
            const clone = this._cell.cloneOutputArea();
            this.addWidget(clone);
        });
    }
    /**
     * The index of the cell in the notebook.
     */
    get index() {
        return this._cell
            ? _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.findFirstIndex(this._notebook.content.widgets, c => c === this._cell)
            : this._index;
    }
    /**
     * The path of the notebook for the cloned output area.
     */
    get path() {
        return this._notebook.context.path;
    }
}
/*
Here we add the singleton PretJupyterHandler to the given editor (context)
 */
function registerPretJupyterHandler(context, rendermime, renderers) {
    const ensureManager = () => {
        if (manager) {
            return manager;
        }
        const instance = new _manager__WEBPACK_IMPORTED_MODULE_15__["default"](context, SETTINGS);
        // @ts-ignore
        window.pretManager = instance;
        contextToPretJupyterHandlerRegistry.set(context, instance);
        manager = instance;
        return instance;
    };
    let manager = contextToPretJupyterHandlerRegistry.get(context);
    for (const r of renderers) {
        r.manager = ensureManager();
    }
    // Replace the placeholder widget renderer with one bound to this widget
    // manager.
    rendermime.removeMimeType(MIMETYPE);
    rendermime.addFactory({
        safe: true,
        mimeTypes: [MIMETYPE],
        // @ts-ignore
        createRenderer: options => new _widget__WEBPACK_IMPORTED_MODULE_16__.PretViewWidget(options, ensureManager())
    }, 0);
    return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_3__.DisposableDelegate(() => {
        if (rendermime) {
            rendermime.removeMimeType(MIMETYPE);
        }
        if (manager) {
            manager.dispose();
        }
    });
}
function registerOutputListener(notebook, listener) {
    let callbacks = [];
    notebook.model.cells.changed.connect((cells, changes) => {
        changes.newValues.forEach((cell) => {
            var _a;
            const signal = (_a = cell === null || cell === void 0 ? void 0 : cell.outputs) === null || _a === void 0 ? void 0 : _a.changed;
            if (!signal)
                return;
            const callback = (outputArea, outputChanges) => {
                for (let index = 0; index < notebook.model.cells.length; index++) {
                    if (cell === notebook.model.cells.get(index)) {
                        const detachPret = outputChanges.newValues.some(outputModel => { var _a, _b; return !!((_b = (_a = outputModel._rawData) === null || _a === void 0 ? void 0 : _a[MIMETYPE]) === null || _b === void 0 ? void 0 : _b['detach']); });
                        if (detachPret) {
                            listener(notebook.parent.context.path, index);
                        }
                    }
                }
            };
            callbacks.push({ callback, signal });
            signal.connect(callback);
        });
        changes.oldValues.forEach((cell) => {
            var _a;
            const oldSignal = (_a = cell === null || cell === void 0 ? void 0 : cell.outputs) === null || _a === void 0 ? void 0 : _a.changed;
            if (!oldSignal)
                return;
            callbacks = callbacks.filter(({ callback, signal }) => {
                if (signal === oldSignal) {
                    signal.disconnect(callback);
                    return false;
                }
                return true;
            });
        });
        //if (change.type == "remove") {
        //
        //}
        // for (const cell of sender.widgets) {
        //     if (cell.model.type === 'code' && (cell as CodeCell).outputArea) {
        //         const signal = (cell as CodeCell).outputArea.outputTracker.widgetAdded;
        //         signal.connect((...args) => {
        //             return listener(cell, (cell as CodeCell).outputArea)
        //         });
        //     }
        // }
    });
}
/*
Activate the extension:
-
 */
function activatePretExtension(app, rendermime, docManager, notebookTracker, settingRegistry, menu, loggerRegistry, restorer) {
    return __awaiter(this, void 0, void 0, function* () {
        const { commands, shell, contextMenu } = app;
        const pretAreas = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_9__.WidgetTracker({
            namespace: 'pret-areas'
        });
        if (restorer) {
            restorer.restore(pretAreas, {
                command: 'pret:create-view',
                args: widget => ({
                    path: widget.content.path,
                    index: widget.content.index,
                }),
                name: widget => `${widget.content.path}:${widget.content.index}`,
                when: notebookTracker.restored // After the notebook widgets (but not contents).
            });
        }
        const bindUnhandledIOPubMessageSignal = (nb) => {
            if (!loggerRegistry) {
                return;
            }
            const wManager = contextToPretJupyterHandlerRegistry[nb.context];
            // Don't know what it is
            if (wManager) {
                wManager.onUnhandledIOPubMessage.connect((sender, msg) => {
                    const logger = loggerRegistry.getLogger(nb.context.path);
                    let level = 'warning';
                    if (_jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.KernelMessage.isErrorMsg(msg) ||
                        (_jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.KernelMessage.isStreamMsg(msg) && msg.content.name === 'stderr')) {
                        level = 'error';
                    }
                    const data = Object.assign(Object.assign({}, msg.content), { output_type: msg.header.msg_type });
                    logger.rendermime = nb.content.rendermime;
                    logger.log({ type: 'output', data, level });
                });
            }
        };
        // Some settings stuff, haven't used it yet
        if (settingRegistry !== null) {
            settingRegistry
                .load(plugin.id)
                .then((settings) => {
                settings.changed.connect(updateSettings);
                updateSettings(settings);
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        // Sets the renderer everytime we see our special SpanComponent/TableEditor mimetype
        rendermime.addFactory({
            safe: false,
            mimeTypes: [MIMETYPE],
            // @ts-ignore
            createRenderer: (options => {
                new _widget__WEBPACK_IMPORTED_MODULE_16__.PretViewWidget(options, null);
            })
        }, 0);
        // Adds the singleton PretJupyterHandler to all existing widgets in the labapp/notebook
        if (notebookTracker !== null) {
            notebookTracker.forEach((panel) => {
                registerPretJupyterHandler(panel.context, panel.content.rendermime, chain(
                // @ts-ignore
                getWidgetsFromNotebook(panel.content), getLinkedWidgetsFromApp(app, panel.sessionContext.path)));
                bindUnhandledIOPubMessageSignal(panel);
            });
            notebookTracker.widgetAdded.connect((sender, panel) => {
                registerPretJupyterHandler(panel.context, panel.content.rendermime, chain(getWidgetsFromNotebook(panel.content), getLinkedWidgetsFromApp(app, panel.sessionContext.path)));
                bindUnhandledIOPubMessageSignal(panel);
            });
            notebookTracker.currentChanged.connect((sender, panel) => {
                registerOutputListener(panel.content, (path, index) => {
                    commands.execute('pret:create-view', { path, index });
                    panel.content.widgets[index].outputHidden = true;
                });
            });
        }
        const widgetTracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_9__.WidgetTracker({ namespace: '' });
        /*if (widgetTracker !== null) {
            widgetTracker.widgetAdded.connect((sender, widget) => {
                console.log(sender, widget);
            })
        }*/
        // -----------------
        // Add some commands
        // -----------------
        if (settingRegistry !== null) {
            // Add a command for automatically saving pret state.
            commands.addCommand('pret:saveAnnotatorState', {
                label: 'Save Annotator State Automatically',
                execute: () => {
                    return settingRegistry
                        .set(plugin.id, 'saveState', !SETTINGS.saveState)
                        .catch((reason) => {
                        console.error(`Failed to set ${plugin.id}: ${reason.message}`);
                    });
                },
                isToggled: () => SETTINGS.saveState
            });
        }
        if (menu) {
            menu.settingsMenu.addGroup([
                { command: 'pret:saveAnnotatorState' }
            ]);
        }
        /**
         * Whether there is an active notebook.
         */
        function isEnabled() {
            return (notebookTracker.currentWidget !== null &&
                notebookTracker.currentWidget === shell.currentWidget);
        }
        /**
         * Whether there is a notebook active, with a single selected cell.
         */
        function isEnabledAndSingleSelected() {
            if (!isEnabled()) {
                return false;
            }
            const { content } = notebookTracker.currentWidget;
            const index = content.activeCellIndex;
            // If there are selections that are not the active cell,
            // this command is confusing, so disable it.
            for (let i = 0; i < content.widgets.length; ++i) {
                if (content.isSelected(content.widgets[i]) && i !== index) {
                    return false;
                }
            }
            return true;
        }
        // CodeCell context menu groups
        contextMenu.addItem({
            command: 'pret:create-view',
            selector: '.jp-Notebook .jp-CodeCell',
            rank: 10.5,
        });
        commands.addCommand('pret:create-view', {
            label: 'Detach',
            execute: (args) => __awaiter(this, void 0, void 0, function* () {
                var _a;
                let cell;
                let current;
                // If we are given a notebook path and cell index, then
                // use that, otherwise use the current active cell.
                const path = args.path;
                let index = args.index;
                if (path && index !== undefined && index !== null) {
                    current = docManager.findWidget(path, 'Notebook');
                    if (!current) {
                        return;
                    }
                }
                else {
                    current = notebookTracker.currentWidget;
                    if (!current) {
                        return;
                    }
                    cell = current.content.activeCell;
                    index = current.content.activeCellIndex;
                }
                // Create a MainAreaWidget
                const content = new PretClonedArea({
                    notebook: current,
                    cell,
                    index,
                });
                // Check if it already exists
                const hasBeenDetached = !!pretAreas.find(widget => (widget.content.path === path)
                    && (widget.content.index === index));
                if (hasBeenDetached) {
                    return;
                }
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_9__.MainAreaWidget({ content });
                current.context.addSibling(widget, {
                    ref: current.id,
                    mode: 'split-bottom'
                });
                const updateCloned = () => {
                    void pretAreas.save(widget);
                };
                current.context.pathChanged.connect(updateCloned);
                (_a = current.context.model) === null || _a === void 0 ? void 0 : _a.cells.changed.connect(updateCloned);
                // Add the cloned output to the output widget tracker.
                void pretAreas.add(widget);
                void pretAreas.save(widget);
                // Remove the output view if the parent notebook is closed.
                current.content.disposed.connect(() => {
                    var _a;
                    current.context.pathChanged.disconnect(updateCloned);
                    (_a = current.context.model) === null || _a === void 0 ? void 0 : _a.cells.changed.disconnect(updateCloned);
                    widget.dispose();
                });
                yield Promise.all([
                    commands.execute("notebook:hide-cell-outputs", args),
                ]);
            }),
            isEnabled: isEnabledAndSingleSelected
        });
        return null;
    });
}
function updateSettings(settings) {
    SETTINGS.saveState = !!settings.get('saveState').composite;
}
const plugin = {
    id: 'pret:plugin', // app
    requires: [
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8__.IRenderMimeRegistry, // rendermime
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_5__.IDocumentManager,
    ],
    optional: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.INotebookTracker, // notebookTracker
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_11__.ISettingRegistry, // settingRegistry
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__.IMainMenu, // menu
        _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_7__.ILoggerRegistry, // loggerRegistry
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_12__.ILayoutRestorer, // restorer
    ],
    activate: activatePretExtension,
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./client/jupyter/style.css":
/*!**********************************!*\
  !*** ./client/jupyter/style.css ***!
  \**********************************/
/***/ ((__unused_webpack_module, __unused_webpack___webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./client/jupyter/style.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* unused harmony default export */ var __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./client/jupyter/widget.tsx":
/*!***********************************!*\
  !*** ./client/jupyter/widget.tsx ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PretViewWidget: () => (/* binding */ PretViewWidget)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _components_Loading__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../components/Loading */ "./client/components/Loading/index.tsx");
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};





/**
 * A renderer for pret Views with Jupyter (Lumino) framework
 */
class ErrorBoundary extends (react__WEBPACK_IMPORTED_MODULE_1___default().Component) {
    constructor(props) {
        super(props);
        this.state = { error: null };
    }
    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { error: error };
    }
    render() {
        if (this.state.error) {
            // You can render any custom fallback UI
            return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("pre", { children: this.state.error.toString() });
        }
        return this.props.children;
    }
}
class PretViewWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor(options, manager) {
        super();
        this.makeView = null;
        this._mimeType = options.mimeType;
        this._viewData = options.view_data;
        this.manager = manager;
        this.keepHiddenWhenExecuted = true;
        this.model = null;
        // Widget will either show up "immediately", ie as soon as the manager is ready,
        // or this method will return prematurely (no view_id/view_type/model) and will
        // wait for the mimetype manager to assign a model to this view and call renderModel
        // on its own (which will call showContent)
        this.addClass("pret-view");
        this.showContent();
    }
    get viewData() {
        if (!this._viewData && this.model) {
            const source = this.model.data[this._mimeType];
            this._viewData = source["view_data"];
        }
        return this._viewData;
    }
    setFlag(flag) {
        const wasVisible = this.isVisible;
        super.setFlag(flag);
        if (this.isVisible && !wasVisible) {
            this.showContent();
        }
        else if (!this.isVisible && wasVisible) {
            this.hideContent();
        }
    }
    clearFlag(flag) {
        const wasVisible = this.isVisible;
        super.clearFlag(flag);
        if (this.isVisible && !wasVisible) {
            this.showContent();
        }
        else if (!this.isVisible && wasVisible) {
            this.hideContent();
        }
    }
    renderModel(model) {
        return __awaiter(this, void 0, void 0, function* () {
            this.model = model;
            this.showContent();
        });
    }
    hideContent() {
        if (!this.isVisible && this._isRendered) {
            react_dom__WEBPACK_IMPORTED_MODULE_2___default().unmountComponentAtNode(this.node);
            this._isRendered = false;
        }
    }
    showContent() {
        if (!this.isVisible) {
            return;
        }
        if (this._isRendered) {
            react_dom__WEBPACK_IMPORTED_MODULE_2___default().unmountComponentAtNode(this.node);
            this._isRendered = false;
        }
        const Render = () => {
            if (!this.makeView) {
                throw this.manager.ready.then(() => {
                    try {
                        this.makeView = this.manager.unpackView(this.viewData);
                    }
                    catch (e) {
                        console.error(e);
                        this.makeView = () => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("code", { children: e.toString() });
                    }
                });
            }
            return this.makeView();
        };
        react_dom__WEBPACK_IMPORTED_MODULE_2___default().render((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(ErrorBoundary, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react__WEBPACK_IMPORTED_MODULE_1__.Suspense, { fallback: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_Loading__WEBPACK_IMPORTED_MODULE_4__["default"], {}), children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(Render, {}) }) }), this.node);
        this._isRendered = true;
    }
}


/***/ }),

/***/ "./client/org.transcrypt.__runtime__.js":
/*!**********************************************!*\
  !*** ./client/org.transcrypt.__runtime__.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AssertionError: () => (/* binding */ AssertionError),
/* harmony export */   AttributeError: () => (/* binding */ AttributeError),
/* harmony export */   BaseException: () => (/* binding */ BaseException),
/* harmony export */   DeprecationWarning: () => (/* binding */ DeprecationWarning),
/* harmony export */   Exception: () => (/* binding */ Exception),
/* harmony export */   IndexError: () => (/* binding */ IndexError),
/* harmony export */   IterableError: () => (/* binding */ IterableError),
/* harmony export */   KeyError: () => (/* binding */ KeyError),
/* harmony export */   NotImplementedError: () => (/* binding */ NotImplementedError),
/* harmony export */   RuntimeWarning: () => (/* binding */ RuntimeWarning),
/* harmony export */   StopIteration: () => (/* binding */ StopIteration),
/* harmony export */   UserWarning: () => (/* binding */ UserWarning),
/* harmony export */   ValueError: () => (/* binding */ ValueError),
/* harmony export */   Warning: () => (/* binding */ Warning),
/* harmony export */   __JsIterator__: () => (/* binding */ __JsIterator__),
/* harmony export */   __PyIterator__: () => (/* binding */ __PyIterator__),
/* harmony export */   __Terminal__: () => (/* binding */ __Terminal__),
/* harmony export */   __add__: () => (/* binding */ __add__),
/* harmony export */   __and__: () => (/* binding */ __and__),
/* harmony export */   __call__: () => (/* binding */ __call__),
/* harmony export */   __envir__: () => (/* binding */ __envir__),
/* harmony export */   __eq__: () => (/* binding */ __eq__),
/* harmony export */   __floordiv__: () => (/* binding */ __floordiv__),
/* harmony export */   __ge__: () => (/* binding */ __ge__),
/* harmony export */   __get__: () => (/* binding */ __get__),
/* harmony export */   __getcm__: () => (/* binding */ __getcm__),
/* harmony export */   __getitem__: () => (/* binding */ __getitem__),
/* harmony export */   __getslice__: () => (/* binding */ __getslice__),
/* harmony export */   __getsm__: () => (/* binding */ __getsm__),
/* harmony export */   __gt__: () => (/* binding */ __gt__),
/* harmony export */   __i__: () => (/* binding */ __i__),
/* harmony export */   __iadd__: () => (/* binding */ __iadd__),
/* harmony export */   __iand__: () => (/* binding */ __iand__),
/* harmony export */   __idiv__: () => (/* binding */ __idiv__),
/* harmony export */   __ijsmod__: () => (/* binding */ __ijsmod__),
/* harmony export */   __ilshift__: () => (/* binding */ __ilshift__),
/* harmony export */   __imatmul__: () => (/* binding */ __imatmul__),
/* harmony export */   __imod__: () => (/* binding */ __imod__),
/* harmony export */   __imul__: () => (/* binding */ __imul__),
/* harmony export */   __in__: () => (/* binding */ __in__),
/* harmony export */   __init__: () => (/* binding */ __init__),
/* harmony export */   __ior__: () => (/* binding */ __ior__),
/* harmony export */   __ipow__: () => (/* binding */ __ipow__),
/* harmony export */   __irshift__: () => (/* binding */ __irshift__),
/* harmony export */   __isub__: () => (/* binding */ __isub__),
/* harmony export */   __ixor__: () => (/* binding */ __ixor__),
/* harmony export */   __jsUsePyNext__: () => (/* binding */ __jsUsePyNext__),
/* harmony export */   __jsmod__: () => (/* binding */ __jsmod__),
/* harmony export */   __k__: () => (/* binding */ __k__),
/* harmony export */   __kwargtrans__: () => (/* binding */ __kwargtrans__),
/* harmony export */   __le__: () => (/* binding */ __le__),
/* harmony export */   __lshift__: () => (/* binding */ __lshift__),
/* harmony export */   __lt__: () => (/* binding */ __lt__),
/* harmony export */   __matmul__: () => (/* binding */ __matmul__),
/* harmony export */   __mergefields__: () => (/* binding */ __mergefields__),
/* harmony export */   __mergekwargtrans__: () => (/* binding */ __mergekwargtrans__),
/* harmony export */   __mod__: () => (/* binding */ __mod__),
/* harmony export */   __mul__: () => (/* binding */ __mul__),
/* harmony export */   __ne__: () => (/* binding */ __ne__),
/* harmony export */   __neg__: () => (/* binding */ __neg__),
/* harmony export */   __nest__: () => (/* binding */ __nest__),
/* harmony export */   __or__: () => (/* binding */ __or__),
/* harmony export */   __pow__: () => (/* binding */ __pow__),
/* harmony export */   __pragma__: () => (/* binding */ __pragma__),
/* harmony export */   __proxy__: () => (/* binding */ __proxy__),
/* harmony export */   __pyUseJsNext__: () => (/* binding */ __pyUseJsNext__),
/* harmony export */   __rshift__: () => (/* binding */ __rshift__),
/* harmony export */   __setitem__: () => (/* binding */ __setitem__),
/* harmony export */   __setproperty__: () => (/* binding */ __setproperty__),
/* harmony export */   __setslice__: () => (/* binding */ __setslice__),
/* harmony export */   __sort__: () => (/* binding */ __sort__),
/* harmony export */   __specialattrib__: () => (/* binding */ __specialattrib__),
/* harmony export */   __sub__: () => (/* binding */ __sub__),
/* harmony export */   __super__: () => (/* binding */ __super__),
/* harmony export */   __t__: () => (/* binding */ __t__),
/* harmony export */   __terminal__: () => (/* binding */ __terminal__),
/* harmony export */   __truediv__: () => (/* binding */ __truediv__),
/* harmony export */   __withblock__: () => (/* binding */ __withblock__),
/* harmony export */   __xor__: () => (/* binding */ __xor__),
/* harmony export */   _class_: () => (/* binding */ _class_),
/* harmony export */   abs: () => (/* binding */ abs),
/* harmony export */   all: () => (/* binding */ all),
/* harmony export */   any: () => (/* binding */ any),
/* harmony export */   assert: () => (/* binding */ assert),
/* harmony export */   bool: () => (/* binding */ bool),
/* harmony export */   bytearray: () => (/* binding */ bytearray),
/* harmony export */   bytes: () => (/* binding */ bytes),
/* harmony export */   callable: () => (/* binding */ callable),
/* harmony export */   chr: () => (/* binding */ chr),
/* harmony export */   copy: () => (/* binding */ copy),
/* harmony export */   deepcopy: () => (/* binding */ deepcopy),
/* harmony export */   delattr: () => (/* binding */ delattr),
/* harmony export */   dict: () => (/* binding */ dict),
/* harmony export */   dir: () => (/* binding */ dir),
/* harmony export */   divmod: () => (/* binding */ divmod),
/* harmony export */   enumerate: () => (/* binding */ enumerate),
/* harmony export */   filter: () => (/* binding */ filter),
/* harmony export */   float: () => (/* binding */ float),
/* harmony export */   getattr: () => (/* binding */ getattr),
/* harmony export */   hasattr: () => (/* binding */ hasattr),
/* harmony export */   input: () => (/* binding */ input),
/* harmony export */   int: () => (/* binding */ int),
/* harmony export */   isinstance: () => (/* binding */ isinstance),
/* harmony export */   issubclass: () => (/* binding */ issubclass),
/* harmony export */   len: () => (/* binding */ len),
/* harmony export */   list: () => (/* binding */ list),
/* harmony export */   map: () => (/* binding */ map),
/* harmony export */   max: () => (/* binding */ max),
/* harmony export */   min: () => (/* binding */ min),
/* harmony export */   object: () => (/* binding */ object),
/* harmony export */   ord: () => (/* binding */ ord),
/* harmony export */   pow: () => (/* binding */ pow),
/* harmony export */   print: () => (/* binding */ print),
/* harmony export */   property: () => (/* binding */ property),
/* harmony export */   py_TypeError: () => (/* binding */ py_TypeError),
/* harmony export */   py_iter: () => (/* binding */ py_iter),
/* harmony export */   py_metatype: () => (/* binding */ py_metatype),
/* harmony export */   py_next: () => (/* binding */ py_next),
/* harmony export */   py_reversed: () => (/* binding */ py_reversed),
/* harmony export */   py_typeof: () => (/* binding */ py_typeof),
/* harmony export */   range: () => (/* binding */ range),
/* harmony export */   repr: () => (/* binding */ repr),
/* harmony export */   round: () => (/* binding */ round),
/* harmony export */   set: () => (/* binding */ set),
/* harmony export */   setattr: () => (/* binding */ setattr),
/* harmony export */   sorted: () => (/* binding */ sorted),
/* harmony export */   str: () => (/* binding */ str),
/* harmony export */   sum: () => (/* binding */ sum),
/* harmony export */   tuple: () => (/* binding */ tuple),
/* harmony export */   zip: () => (/* binding */ zip)
/* harmony export */ });
// Transcrypt'ed from Python, 2025-06-02 17:59:31
var __name__ = 'org.transcrypt.__runtime__';
var __envir__ = {};
__envir__.interpreter_name = 'python';
__envir__.transpiler_name = 'transcrypt';
__envir__.executor_name = __envir__.transpiler_name;
__envir__.transpiler_version = '3.7.16';
function __nest__(headObject, tailNames, value) {
    var current = headObject;
    if (tailNames != '') {
        var tailChain = tailNames.split('.');
        var firstNewIndex = tailChain.length;
        for (var index = 0; index < tailChain.length; index++) {
            if (!current.hasOwnProperty(tailChain[index])) {
                firstNewIndex = index;
                break;
            }
            current = current[tailChain[index]];
        }
        for (var index = firstNewIndex; index < tailChain.length; index++) {
            current[tailChain[index]] = {};
            current = current[tailChain[index]];
        }
    }
    for (let attrib of Object.getOwnPropertyNames(value)) {
        Object.defineProperty(current, attrib, {
            get() { return value[attrib]; },
            enumerable: true,
            configurable: true
        });
    }
}
;
function __init__(module) {
    if (!module.__inited__) {
        module.__all__.__init__(module.__all__);
        module.__inited__ = true;
    }
    return module.__all__;
}
;
var __proxy__ = false;
function __get__(self, func, quotedFuncName) {
    if (self) {
        if (self.hasOwnProperty('__class__') || typeof self == 'string' || self instanceof String) {
            if (quotedFuncName) {
                Object.defineProperty(self, quotedFuncName, {
                    value: function () {
                        var args = [].slice.apply(arguments);
                        return func.apply(null, [self].concat(args));
                    },
                    writable: true,
                    enumerable: true,
                    configurable: true
                });
            }
            return function () {
                var args = [].slice.apply(arguments);
                return func.apply(null, [self].concat(args));
            };
        }
        else {
            return func;
        }
    }
    else {
        return func;
    }
}
;
function __getcm__(self, func, quotedFuncName) {
    if (self.hasOwnProperty('__class__')) {
        return function () {
            var args = [].slice.apply(arguments);
            return func.apply(null, [self.__class__].concat(args));
        };
    }
    else {
        return function () {
            var args = [].slice.apply(arguments);
            return func.apply(null, [self].concat(args));
        };
    }
}
;
function __getsm__(self, func, quotedFuncName) {
    return func;
}
;
var py_metatype = {
    __name__: 'type',
    __bases__: [],
    __new__: function (meta, name, bases, attribs) {
        var cls = function () {
            var args = [].slice.apply(arguments);
            var instance = cls.__new__(args);
            cls.__init__.apply(null, [instance].concat(args));
            return instance;
        };
        for (var index = bases.length - 1; index >= 0; index--) {
            var base = bases[index];
            for (var attrib in base) {
                var descrip = Object.getOwnPropertyDescriptor(base, attrib);
                Object.defineProperty(cls, attrib, descrip);
            }
            for (let symbol of Object.getOwnPropertySymbols(base)) {
                let descrip = Object.getOwnPropertyDescriptor(base, symbol);
                Object.defineProperty(cls, symbol, descrip);
            }
        }
        cls.__metaclass__ = meta;
        cls.__name__ = name.startsWith('py_') ? name.slice(3) : name;
        cls.__bases__ = bases;
        for (var attrib in attribs) {
            var descrip = Object.getOwnPropertyDescriptor(attribs, attrib);
            Object.defineProperty(cls, attrib, descrip);
        }
        for (let symbol of Object.getOwnPropertySymbols(attribs)) {
            let descrip = Object.getOwnPropertyDescriptor(attribs, symbol);
            Object.defineProperty(cls, symbol, descrip);
        }
        return cls;
    }
};
py_metatype.__metaclass__ = py_metatype;
var object = {
    __init__: function (self) { },
    __metaclass__: py_metatype,
    __name__: 'object',
    __bases__: [],
    __new__: function (args) {
        var instance = Object.create(this, { __class__: { value: this, enumerable: true } });
        if ('__getattr__' in this || '__setattr__' in this) {
            instance = new Proxy(instance, {
                get: function (target, name) {
                    let result = target[name];
                    if (result == undefined) {
                        return target.__getattr__(name);
                    }
                    else {
                        return result;
                    }
                },
                set: function (target, name, value) {
                    try {
                        target.__setattr__(name, value);
                    }
                    catch (exception) {
                        target[name] = value;
                    }
                    return true;
                }
            });
        }
        return instance;
    }
};
function _class_(name, bases, attribs, meta) {
    if (meta === undefined) {
        meta = bases[0].__metaclass__;
    }
    return meta.__new__(meta, name, bases, attribs);
}
;
function __pragma__() { }
;
function __call__( /* <callee>, <this>, <params>* */) {
    var args = [].slice.apply(arguments);
    if (typeof args[0] == 'object' && '__call__' in args[0]) {
        return args[0].__call__.apply(args[1], args.slice(2));
    }
    else {
        return args[0].apply(args[1], args.slice(2));
    }
}
;
__envir__.executor_name = __envir__.transpiler_name;
var __main__ = { __file__: '' };
var __except__ = null;
function __kwargtrans__(anObject) {
    anObject.__kwargtrans__ = null;
    Object.defineProperty(anObject, 'constructor', { value: Object, writable: false, enumerable: false, configurable: false });
    return anObject;
}
function __super__(aClass, methodName) {
    for (let base of aClass.__bases__) {
        if (methodName in base) {
            return base[methodName];
        }
    }
    throw new Exception('Superclass method not found');
}
function property(getter, setter) {
    if (!setter) {
        setter = function () { };
    }
    return { get: function () { return getter(this); }, set: function (value) { setter(this, value); }, enumerable: true };
}
function __setproperty__(anObject, name, descriptor) {
    if (!anObject.hasOwnProperty(name)) {
        Object.defineProperty(anObject, name, descriptor);
    }
}
function assert(condition, message) {
    if (!condition) {
        throw AssertionError(message, new Error());
    }
}
function __mergekwargtrans__(object0, object1) {
    var result = {};
    for (var attrib in object0) {
        result[attrib] = object0[attrib];
    }
    for (var attrib in object1) {
        result[attrib] = object1[attrib];
    }
    return result;
}
;
function __mergefields__(targetClass, sourceClass) {
    let fieldNames = ['__reprfields__', '__comparefields__', '__initfields__'];
    if (sourceClass[fieldNames[0]]) {
        if (targetClass[fieldNames[0]]) {
            for (let fieldName of fieldNames) {
                targetClass[fieldName] = new Set([...targetClass[fieldName], ...sourceClass[fieldName]]);
            }
        }
        else {
            for (let fieldName of fieldNames) {
                targetClass[fieldName] = new Set(sourceClass[fieldName]);
            }
        }
    }
}
function __withblock__(manager, statements) {
    if (hasattr(manager, '__enter__')) {
        try {
            manager.__enter__();
            statements();
            manager.__exit__();
        }
        catch (exception) {
            if (!(manager.__exit__(exception.name, exception, exception.stack))) {
                throw exception;
            }
        }
    }
    else {
        statements();
        manager.close();
    }
}
;
function dir(obj) {
    var aList = [];
    for (var aKey in obj) {
        aList.push(aKey.startsWith('py_') ? aKey.slice(3) : aKey);
    }
    aList.sort();
    return aList;
}
;
function setattr(obj, name, value) {
    obj[name] = value;
}
;
function getattr(obj, name) {
    return name in obj ? obj[name] : obj['py_' + name];
}
;
function hasattr(obj, name) {
    try {
        return name in obj || 'py_' + name in obj;
    }
    catch (exception) {
        return false;
    }
}
;
function delattr(obj, name) {
    if (name in obj) {
        delete obj[name];
    }
    else {
        delete obj['py_' + name];
    }
}
;
function __in__(element, container) {
    if (container === undefined || container === null) {
        return false;
    }
    if (container.indexOf) {
        return container.indexOf(element) > -1;
    }
    if (container.__contains__ instanceof Function) {
        return container.__contains__(element);
    }
    else {
        return container.hasOwnProperty(element);
    }
}
;
function __specialattrib__(attrib) {
    return (attrib.startswith('__') && attrib.endswith('__')) || attrib == 'constructor' || attrib.startswith('py_');
}
;
function len(anObject) {
    if (anObject === undefined || anObject === null) {
        return 0;
    }
    if (anObject.__len__ instanceof Function) {
        return anObject.__len__();
    }
    if (anObject.length !== undefined) {
        return anObject.length;
    }
    var length = 0;
    for (var attr in anObject) {
        if (!__specialattrib__(attr)) {
            length++;
        }
    }
    return length;
}
;
function __i__(any) {
    return py_typeof(any) == dict ? any.py_keys() : any;
}
function __k__(keyed, key) {
    var result = keyed[key];
    if (typeof result == 'undefined') {
        if (keyed instanceof Array)
            if (key == +key && key >= 0 && keyed.length > key)
                return result;
            else
                throw IndexError(key, new Error());
        else
            throw KeyError(key, new Error());
    }
    return result;
}
function __t__(target) {
    return (target === undefined || target === null ? false :
        ['boolean', 'number'].indexOf(typeof target) >= 0 ? target :
            target.__bool__ instanceof Function ? (target.__bool__() ? target : false) :
                target.__len__ instanceof Function ? (target.__len__() !== 0 ? target : false) :
                    target instanceof Function ? target :
                        len(target) !== 0 ? target :
                            false);
}
function float(any) {
    if (any == 'inf') {
        return Infinity;
    }
    else if (any == '-inf') {
        return -Infinity;
    }
    else if (any == 'nan') {
        return NaN;
    }
    else if (isNaN(parseFloat(any))) {
        if (any === false) {
            return 0;
        }
        else if (any === true) {
            return 1;
        }
        else {
            throw ValueError("could not convert string to float: '" + str(any) + "'", new Error());
        }
    }
    else {
        return +any;
    }
}
;
float.__name__ = 'float';
float.__bases__ = [object];
function int(any) {
    return float(any) | 0;
}
;
int.__name__ = 'int';
int.__bases__ = [object];
function bool(any) {
    return !!__t__(any);
}
;
bool.__name__ = 'bool';
bool.__bases__ = [int];
function py_typeof(anObject) {
    var aType = typeof anObject;
    if (aType == 'object') {
        try {
            return '__class__' in anObject ? anObject.__class__ : object;
        }
        catch (exception) {
            return aType;
        }
    }
    else {
        return (aType == 'boolean' ? bool :
            aType == 'string' ? str :
                aType == 'number' ? (anObject % 1 == 0 ? int : float) :
                    null);
    }
}
;
function issubclass(aClass, classinfo) {
    if (classinfo instanceof Array) {
        for (let aClass2 of classinfo) {
            if (issubclass(aClass, aClass2)) {
                return true;
            }
        }
        return false;
    }
    try {
        var aClass2 = aClass;
        if (aClass2 == classinfo) {
            return true;
        }
        else {
            var bases = [].slice.call(aClass2.__bases__);
            while (bases.length) {
                aClass2 = bases.shift();
                if (aClass2 == classinfo) {
                    return true;
                }
                if (aClass2.__bases__.length) {
                    bases = [].slice.call(aClass2.__bases__).concat(bases);
                }
            }
            return false;
        }
    }
    catch (exception) {
        return aClass == classinfo || classinfo == object;
    }
}
;
function isinstance(anObject, classinfo) {
    try {
        return '__class__' in anObject ? issubclass(anObject.__class__, classinfo) : issubclass(py_typeof(anObject), classinfo);
    }
    catch (exception) {
        return issubclass(py_typeof(anObject), classinfo);
    }
}
;
function callable(anObject) {
    return anObject && typeof anObject == 'object' && '__call__' in anObject ? true : typeof anObject === 'function';
}
;
function repr(anObject) {
    try {
        return anObject.__repr__();
    }
    catch (exception) {
        try {
            return anObject.__str__();
        }
        catch (exception) {
            try {
                if (anObject == null) {
                    return 'None';
                }
                else if (anObject.constructor == Object) {
                    var result = '{';
                    var comma = false;
                    for (var attrib in anObject) {
                        if (!__specialattrib__(attrib)) {
                            if (attrib.isnumeric()) {
                                var attribRepr = attrib;
                            }
                            else {
                                var attribRepr = '\'' + attrib + '\'';
                            }
                            if (comma) {
                                result += ', ';
                            }
                            else {
                                comma = true;
                            }
                            result += attribRepr + ': ' + repr(anObject[attrib]);
                        }
                    }
                    result += '}';
                    return result;
                }
                else {
                    return typeof anObject == 'boolean' ? anObject.toString().capitalize() : anObject.toString();
                }
            }
            catch (exception) {
                return '<object of type: ' + typeof anObject + '>';
            }
        }
    }
}
;
function chr(charCode) {
    return String.fromCharCode(charCode);
}
;
function ord(aChar) {
    return aChar.charCodeAt(0);
}
;
function max(nrOrSeq) {
    return arguments.length == 1 ? Math.max(...nrOrSeq) : Math.max(...arguments);
}
;
function min(nrOrSeq) {
    return arguments.length == 1 ? Math.min(...nrOrSeq) : Math.min(...arguments);
}
;
var abs = Math.abs;
function round(number, ndigits) {
    if (ndigits) {
        var scale = Math.pow(10, ndigits);
        number *= scale;
    }
    var rounded = Math.round(number);
    if (rounded - number == 0.5 && rounded % 2) {
        rounded -= 1;
    }
    if (ndigits) {
        rounded /= scale;
    }
    return rounded;
}
;
function __jsUsePyNext__() {
    try {
        var result = this.__next__();
        return { value: result, done: false };
    }
    catch (exception) {
        return { value: undefined, done: true };
    }
}
function __pyUseJsNext__() {
    var result = this.next();
    if (result.done) {
        throw StopIteration(new Error());
    }
    else {
        return result.value;
    }
}
function py_iter(iterable) {
    if (typeof iterable == 'string' || '__iter__' in iterable) {
        var result = iterable.__iter__();
        result.next = __jsUsePyNext__;
    }
    else if ('selector' in iterable) {
        var result = list(iterable).__iter__();
        result.next = __jsUsePyNext__;
    }
    else if ('next' in iterable) {
        var result = iterable;
        if (!('__next__' in result)) {
            result.__next__ = __pyUseJsNext__;
        }
    }
    else if (Symbol.iterator in iterable) {
        var result = iterable[Symbol.iterator]();
        result.__next__ = __pyUseJsNext__;
    }
    else {
        throw IterableError(new Error());
    }
    result[Symbol.iterator] = function () { return result; };
    return result;
}
function py_next(iterator) {
    try {
        var result = iterator.__next__();
    }
    catch (exception) {
        var result = iterator.next();
        if (result.done) {
            throw StopIteration(new Error());
        }
        else {
            return result.value;
        }
    }
    if (result == undefined) {
        throw StopIteration(new Error());
    }
    else {
        return result;
    }
}
function __PyIterator__(iterable) {
    this.iterable = iterable;
    this.index = 0;
}
__PyIterator__.prototype.__next__ = function () {
    if (this.index < this.iterable.length) {
        return this.iterable[this.index++];
    }
    else {
        throw StopIteration(new Error());
    }
};
function __JsIterator__(iterable) {
    this.iterable = iterable;
    this.index = 0;
}
__JsIterator__.prototype.next = function () {
    if (this.index < this.iterable.py_keys.length) {
        return { value: this.index++, done: false };
    }
    else {
        return { value: undefined, done: true };
    }
};
function py_reversed(iterable) {
    iterable = iterable.slice();
    iterable.reverse();
    return iterable;
}
;
function zip() {
    var args = [].slice.call(arguments);
    for (var i = 0; i < args.length; i++) {
        if (typeof args[i] == 'string') {
            args[i] = args[i].split('');
        }
        else if (!Array.isArray(args[i])) {
            args[i] = Array.from(args[i]);
        }
    }
    var shortest = args.length == 0 ? [] : args.reduce(function (array0, array1) {
        return array0.length < array1.length ? array0 : array1;
    });
    return shortest.map(function (current, index) {
        return args.map(function (current) {
            return current[index];
        });
    });
}
;
function range(start, stop, step) {
    if (stop == undefined) {
        stop = start;
        start = 0;
    }
    if (step == undefined) {
        step = 1;
    }
    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
        return [];
    }
    var result = [];
    for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
        result.push(i);
    }
    return result;
}
;
function any(iterable) {
    for (let item of iterable) {
        if (bool(item)) {
            return true;
        }
    }
    return false;
}
function all(iterable) {
    for (let item of iterable) {
        if (!bool(item)) {
            return false;
        }
    }
    return true;
}
function sum(iterable) {
    let result = 0;
    for (let item of iterable) {
        result += item;
    }
    return result;
}
function enumerate(iterable) {
    return zip(range(len(iterable)), iterable);
}
function copy(anObject) {
    if (anObject == null || typeof anObject == "object") {
        return anObject;
    }
    else {
        var result = {};
        for (var attrib in obj) {
            if (anObject.hasOwnProperty(attrib)) {
                result[attrib] = anObject[attrib];
            }
        }
        return result;
    }
}
function deepcopy(anObject) {
    if (anObject == null || typeof anObject == "object") {
        return anObject;
    }
    else {
        var result = {};
        for (var attrib in obj) {
            if (anObject.hasOwnProperty(attrib)) {
                result[attrib] = deepcopy(anObject[attrib]);
            }
        }
        return result;
    }
}
function list(iterable) {
    if (Object.getPrototypeOf(iterable).constructor === __PyIterator__) {
        iterable = iterable.iterable;
    }
    let instance = iterable ? Array.from(iterable) : [];
    return instance;
}
Array.prototype.__class__ = list;
list.__name__ = 'list';
list.__bases__ = [object];
Array.prototype.__iter__ = function () { return new __PyIterator__(this); };
Array.prototype.__getslice__ = function (start, stop, step) {
    if (start < 0) {
        start = this.length + start;
    }
    if (stop == null) {
        stop = this.length;
    }
    else if (stop < 0) {
        stop = this.length + stop;
    }
    else if (stop > this.length) {
        stop = this.length;
    }
    if (step == 1) {
        return Array.prototype.slice.call(this, start, stop);
    }
    let result = list([]);
    for (let index = start; index < stop; index += step) {
        result.push(this[index]);
    }
    return result;
};
Array.prototype.__setslice__ = function (start, stop, step, source) {
    if (start < 0) {
        start = this.length + start;
    }
    if (stop == null) {
        stop = this.length;
    }
    else if (stop < 0) {
        stop = this.length + stop;
    }
    if (step == null) {
        Array.prototype.splice.apply(this, [start, stop - start].concat(source));
    }
    else {
        let sourceIndex = 0;
        for (let targetIndex = start; targetIndex < stop; targetIndex += step) {
            this[targetIndex] = source[sourceIndex++];
        }
    }
};
Array.prototype.__repr__ = function () {
    if (this.__class__ == set && !this.length) {
        return 'set()';
    }
    let result = !this.__class__ || this.__class__ == list ? '[' : this.__class__ == tuple ? '(' : '{';
    for (let index = 0; index < this.length; index++) {
        if (index) {
            result += ', ';
        }
        result += repr(this[index]);
    }
    if (this.__class__ == tuple && this.length == 1) {
        result += ',';
    }
    result += !this.__class__ || this.__class__ == list ? ']' : this.__class__ == tuple ? ')' : '}';
    ;
    return result;
};
Array.prototype.__str__ = Array.prototype.__repr__;
Array.prototype.append = function (element) {
    this.push(element);
};
Array.prototype.py_clear = function () {
    this.length = 0;
};
Array.prototype.extend = function (aList) {
    this.push.apply(this, aList);
};
Array.prototype.insert = function (index, element) {
    this.splice(index, 0, element);
};
Array.prototype.remove = function (element) {
    let index = this.indexOf(element);
    if (index == -1) {
        throw ValueError("list.remove(x): x not in list", new Error());
    }
    this.splice(index, 1);
};
Array.prototype.index = function (element) {
    return this.indexOf(element);
};
Array.prototype.py_pop = function (index) {
    if (index == undefined) {
        return this.pop();
    }
    else {
        return this.splice(index, 1)[0];
    }
};
Array.prototype.py_sort = function () {
    __sort__.apply(null, [this].concat([].slice.apply(arguments)));
};
Array.prototype.__add__ = function (aList) {
    return list(this.concat(aList));
};
Array.prototype.__mul__ = function (scalar) {
    let result = this;
    for (let i = 1; i < scalar; i++) {
        result = result.concat(this);
    }
    return result;
};
Array.prototype.__rmul__ = Array.prototype.__mul__;
function tuple(iterable) {
    let instance = iterable ? [].slice.apply(iterable) : [];
    instance.__class__ = tuple;
    return instance;
}
tuple.__name__ = 'tuple';
tuple.__bases__ = [object];
function set(iterable) {
    let instance = [];
    if (iterable) {
        if (Object.getPrototypeOf(iterable).constructor === __PyIterator__) {
            iterable = iterable.iterable;
        }
        for (let index = 0; index < iterable.length; index++) {
            instance.add(iterable[index]);
        }
    }
    instance.__class__ = set;
    return instance;
}
set.__name__ = 'set';
set.__bases__ = [object];
Array.prototype.__bindexOf__ = function (element) {
    element += '';
    let mindex = 0;
    let maxdex = this.length - 1;
    while (mindex <= maxdex) {
        let index = (mindex + maxdex) / 2 | 0;
        let middle = this[index] + '';
        if (middle < element) {
            mindex = index + 1;
        }
        else if (middle > element) {
            maxdex = index - 1;
        }
        else {
            return index;
        }
    }
    return -1;
};
Array.prototype.add = function (element) {
    if (this.indexOf(element) == -1) {
        this.push(element);
    }
};
Array.prototype.discard = function (element) {
    var index = this.indexOf(element);
    if (index != -1) {
        this.splice(index, 1);
    }
};
Array.prototype.isdisjoint = function (other) {
    this.sort();
    for (let i = 0; i < other.length; i++) {
        if (this.__bindexOf__(other[i]) != -1) {
            return false;
        }
    }
    return true;
};
Array.prototype.issuperset = function (other) {
    this.sort();
    for (let i = 0; i < other.length; i++) {
        if (this.__bindexOf__(other[i]) == -1) {
            return false;
        }
    }
    return true;
};
Array.prototype.issubset = function (other) {
    return set(other.slice()).issuperset(this);
};
Array.prototype.union = function (other) {
    let result = set(this.slice().sort());
    for (let i = 0; i < other.length; i++) {
        if (result.__bindexOf__(other[i]) == -1) {
            result.push(other[i]);
        }
    }
    return result;
};
Array.prototype.intersection = function (other) {
    this.sort();
    let result = set();
    for (let i = 0; i < other.length; i++) {
        if (this.__bindexOf__(other[i]) != -1) {
            result.push(other[i]);
        }
    }
    return result;
};
Array.prototype.difference = function (other) {
    let sother = set(other.slice().sort());
    let result = set();
    for (let i = 0; i < this.length; i++) {
        if (sother.__bindexOf__(this[i]) == -1) {
            result.push(this[i]);
        }
    }
    return result;
};
Array.prototype.symmetric_difference = function (other) {
    return this.union(other).difference(this.intersection(other));
};
Array.prototype.py_update = function () {
    let updated = [].concat.apply(this.slice(), arguments).sort();
    this.py_clear();
    for (let i = 0; i < updated.length; i++) {
        if (updated[i] != updated[i - 1]) {
            this.push(updated[i]);
        }
    }
};
Array.prototype.__eq__ = function (other) {
    if (this.length != other.length) {
        return false;
    }
    if (this.__class__ == set) {
        this.sort();
        other.sort();
    }
    for (let i = 0; i < this.length; i++) {
        if (this[i] != other[i]) {
            return false;
        }
    }
    return true;
};
Array.prototype.__ne__ = function (other) {
    return !this.__eq__(other);
};
Array.prototype.__le__ = function (other) {
    if (this.__class__ == set) {
        return this.issubset(other);
    }
    else {
        for (let i = 0; i < this.length; i++) {
            if (this[i] > other[i]) {
                return false;
            }
            else if (this[i] < other[i]) {
                return true;
            }
        }
        return true;
    }
};
Array.prototype.__ge__ = function (other) {
    if (this.__class__ == set) {
        return this.issuperset(other);
    }
    else {
        for (let i = 0; i < this.length; i++) {
            if (this[i] < other[i]) {
                return false;
            }
            else if (this[i] > other[i]) {
                return true;
            }
        }
        return true;
    }
};
Array.prototype.__lt__ = function (other) {
    return (this.__class__ == set ?
        this.issubset(other) && !this.issuperset(other) :
        !this.__ge__(other));
};
Array.prototype.__gt__ = function (other) {
    return (this.__class__ == set ?
        this.issuperset(other) && !this.issubset(other) :
        !this.__le__(other));
};
function bytearray(bytable, encoding) {
    if (bytable == undefined) {
        return new Uint8Array(0);
    }
    else {
        let aType = py_typeof(bytable);
        if (aType == int) {
            return new Uint8Array(bytable);
        }
        else if (aType == str) {
            let aBytes = new Uint8Array(len(bytable));
            for (let i = 0; i < len(bytable); i++) {
                aBytes[i] = bytable.charCodeAt(i);
            }
            return aBytes;
        }
        else if (aType == list || aType == tuple) {
            return new Uint8Array(bytable);
        }
        else {
            throw py_TypeError;
        }
    }
}
var bytes = bytearray;
Uint8Array.prototype.__add__ = function (aBytes) {
    let result = new Uint8Array(this.length + aBytes.length);
    result.set(this);
    result.set(aBytes, this.length);
    return result;
};
Uint8Array.prototype.__mul__ = function (scalar) {
    let result = new Uint8Array(scalar * this.length);
    for (let i = 0; i < scalar; i++) {
        result.set(this, i * this.length);
    }
    return result;
};
Uint8Array.prototype.__rmul__ = Uint8Array.prototype.__mul__;
function str(stringable) {
    if (typeof stringable === 'number')
        return stringable.toString();
    else {
        try {
            return stringable.__str__();
        }
        catch (exception) {
            try {
                return repr(stringable);
            }
            catch (exception) {
                return String(stringable);
            }
        }
    }
}
;
String.prototype.__class__ = str;
str.__name__ = 'str';
str.__bases__ = [object];
String.prototype.__iter__ = function () { new __PyIterator__(this); };
String.prototype.__repr__ = function () {
    return (this.indexOf('\'') == -1 ? '\'' + this + '\'' : '"' + this + '"').py_replace('\t', '\\t').py_replace('\n', '\\n');
};
String.prototype.__str__ = function () {
    return this;
};
String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
};
String.prototype.endswith = function (suffix) {
    if (suffix instanceof Array) {
        for (var i = 0; i < suffix.length; i++) {
            if (this.slice(-suffix[i].length) == suffix[i])
                return true;
        }
    }
    else
        return suffix == '' || this.slice(-suffix.length) == suffix;
    return false;
};
String.prototype.find = function (sub, start) {
    return this.indexOf(sub, start);
};
String.prototype.__getslice__ = function (start, stop, step) {
    if (start < 0) {
        start = this.length + start;
    }
    if (stop == null) {
        stop = this.length;
    }
    else if (stop < 0) {
        stop = this.length + stop;
    }
    var result = '';
    if (step == 1) {
        result = this.substring(start, stop);
    }
    else {
        for (var index = start; index < stop; index += step) {
            result = result.concat(this.charAt(index));
        }
    }
    return result;
};
__setproperty__(String.prototype, 'format', {
    get: function () {
        return __get__(this, function (self) {
            var args = tuple([].slice.apply(arguments).slice(1));
            var autoIndex = 0;
            return self.replace(/\{(\w*)\}/g, function (match, key) {
                if (key == '') {
                    key = autoIndex++;
                }
                if (key == +key) {
                    return args[key] === undefined ? match : str(args[key]);
                }
                else {
                    for (var index = 0; index < args.length; index++) {
                        if (typeof args[index] == 'object' && args[index][key] !== undefined) {
                            return str(args[index][key]);
                        }
                    }
                    return match;
                }
            });
        });
    },
    enumerable: true
});
String.prototype.isalnum = function () {
    return /^[0-9a-zA-Z]{1,}$/.test(this);
};
String.prototype.isalpha = function () {
    return /^[a-zA-Z]{1,}$/.test(this);
};
String.prototype.isdecimal = function () {
    return /^[0-9]{1,}$/.test(this);
};
String.prototype.isdigit = function () {
    return this.isdecimal();
};
String.prototype.islower = function () {
    return /^[a-z]{1,}$/.test(this);
};
String.prototype.isupper = function () {
    return /^[A-Z]{1,}$/.test(this);
};
String.prototype.isspace = function () {
    return /^[\s]{1,}$/.test(this);
};
String.prototype.isnumeric = function () {
    return !isNaN(parseFloat(this)) && isFinite(this);
};
String.prototype.join = function (strings) {
    strings = Array.from(strings);
    return strings.join(this);
};
String.prototype.lower = function () {
    return this.toLowerCase();
};
String.prototype.py_replace = function (old, aNew, maxreplace) {
    return this.split(old, maxreplace).join(aNew);
};
String.prototype.lstrip = function () {
    return this.replace(/^\s*/g, '');
};
String.prototype.rfind = function (sub, start) {
    return this.lastIndexOf(sub, start);
};
String.prototype.rsplit = function (sep, maxsplit) {
    if (sep == undefined || sep == null) {
        sep = /\s+/;
        var stripped = this.strip();
    }
    else {
        var stripped = this;
    }
    if (maxsplit == undefined || maxsplit == -1) {
        return stripped.split(sep);
    }
    else {
        var result = stripped.split(sep);
        if (maxsplit < result.length) {
            var maxrsplit = result.length - maxsplit;
            return [result.slice(0, maxrsplit).join(sep)].concat(result.slice(maxrsplit));
        }
        else {
            return result;
        }
    }
};
String.prototype.rstrip = function () {
    return this.replace(/\s*$/g, '');
};
String.prototype.py_split = function (sep, maxsplit) {
    if (sep == undefined || sep == null) {
        sep = /\s+/;
        var stripped = this.strip();
    }
    else {
        var stripped = this;
    }
    if (maxsplit == undefined || maxsplit == -1) {
        return stripped.split(sep);
    }
    else {
        var result = stripped.split(sep);
        if (maxsplit < result.length) {
            return result.slice(0, maxsplit).concat([result.slice(maxsplit).join(sep)]);
        }
        else {
            return result;
        }
    }
};
String.prototype.startswith = function (prefix) {
    if (prefix instanceof Array) {
        for (var i = 0; i < prefix.length; i++) {
            if (this.indexOf(prefix[i]) == 0)
                return true;
        }
    }
    else
        return this.indexOf(prefix) == 0;
    return false;
};
String.prototype.strip = function () {
    return this.trim();
};
String.prototype.upper = function () {
    return this.toUpperCase();
};
String.prototype.__mul__ = function (scalar) {
    var result = '';
    for (var i = 0; i < scalar; i++) {
        result = result + this;
    }
    return result;
};
String.prototype.__rmul__ = String.prototype.__mul__;
function __contains__(element) {
    return this.hasOwnProperty(element);
}
function __keys__() {
    var keys = [];
    for (var attrib in this) {
        if (!__specialattrib__(attrib)) {
            keys.push(attrib);
        }
    }
    return keys;
}
function __items__() {
    var items = [];
    for (var attrib in this) {
        if (!__specialattrib__(attrib)) {
            items.push([attrib, this[attrib]]);
        }
    }
    return items;
}
function __del__(key) {
    delete this[key];
}
function __clear__() {
    for (var attrib in this) {
        delete this[attrib];
    }
}
function __getdefault__(aKey, aDefault) {
    var result = this[aKey];
    if (result == undefined) {
        result = this['py_' + aKey];
    }
    return result == undefined ? (aDefault == undefined ? null : aDefault) : result;
}
function __setdefault__(aKey, aDefault) {
    var result = this[aKey];
    if (result != undefined) {
        return result;
    }
    var val = aDefault == undefined ? null : aDefault;
    this[aKey] = val;
    return val;
}
function __pop__(aKey, aDefault) {
    var result = this[aKey];
    if (result != undefined) {
        delete this[aKey];
        return result;
    }
    else {
        if (aDefault === undefined) {
            throw KeyError(aKey, new Error());
        }
    }
    return aDefault;
}
function __popitem__() {
    var aKey = Object.keys(this)[0];
    if (aKey == null) {
        throw KeyError("popitem(): dictionary is empty", new Error());
    }
    var result = tuple([aKey, this[aKey]]);
    delete this[aKey];
    return result;
}
function __update__(aDict) {
    for (var aKey in aDict) {
        this[aKey] = aDict[aKey];
    }
}
function __values__() {
    var values = [];
    for (var attrib in this) {
        if (!__specialattrib__(attrib)) {
            values.push(this[attrib]);
        }
    }
    return values;
}
function __dgetitem__(aKey) {
    return this[aKey];
}
function __dsetitem__(aKey, aValue) {
    this[aKey] = aValue;
}
function dict(objectOrPairs) {
    var instance = {};
    if (!objectOrPairs || objectOrPairs instanceof Array) {
        if (objectOrPairs) {
            for (var index = 0; index < objectOrPairs.length; index++) {
                var pair = objectOrPairs[index];
                if (!(pair instanceof Array) || pair.length != 2) {
                    throw ValueError("dict update sequence element #" + index +
                        " has length " + pair.length +
                        "; 2 is required", new Error());
                }
                var key = pair[0];
                var val = pair[1];
                if (!(objectOrPairs instanceof Array) && objectOrPairs instanceof Object) {
                    if (!isinstance(objectOrPairs, dict)) {
                        val = dict(val);
                    }
                }
                instance[key] = val;
            }
        }
    }
    else {
        if (isinstance(objectOrPairs, dict)) {
            var aKeys = objectOrPairs.py_keys();
            for (var index = 0; index < aKeys.length; index++) {
                var key = aKeys[index];
                instance[key] = objectOrPairs[key];
            }
        }
        else if (objectOrPairs instanceof Object) {
            instance = objectOrPairs;
        }
        else {
            throw ValueError("Invalid type of object for dict creation", new Error());
        }
    }
    __setproperty__(instance, '__class__', { value: dict, enumerable: false, writable: true });
    __setproperty__(instance, '__contains__', { value: __contains__, enumerable: false });
    __setproperty__(instance, 'py_keys', { value: __keys__, enumerable: false });
    __setproperty__(instance, '__iter__', { value: function () { new __PyIterator__(this.py_keys()); }, enumerable: false });
    __setproperty__(instance, 'py_items', { value: __items__, enumerable: false });
    __setproperty__(instance, 'py_del', { value: __del__, enumerable: false });
    __setproperty__(instance, 'py_clear', { value: __clear__, enumerable: false });
    __setproperty__(instance, 'py_get', { value: __getdefault__, enumerable: false });
    __setproperty__(instance, 'py_setdefault', { value: __setdefault__, enumerable: false });
    __setproperty__(instance, 'py_pop', { value: __pop__, enumerable: false });
    __setproperty__(instance, 'py_popitem', { value: __popitem__, enumerable: false });
    __setproperty__(instance, 'py_update', { value: __update__, enumerable: false });
    __setproperty__(instance, 'py_values', { value: __values__, enumerable: false });
    __setproperty__(instance, '__getitem__', { value: __dgetitem__, enumerable: false });
    __setproperty__(instance, '__setitem__', { value: __dsetitem__, enumerable: false });
    return instance;
}
Object.defineProperty(Object.prototype, '__contains__', { value: __contains__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_keys', { value: __keys__, enumerable: false });
Object.defineProperty(Object.prototype, '__iter__', { value: function () { new __PyIterator__(this.py_keys()); }, enumerable: false });
Object.defineProperty(Object.prototype, 'py_items', { value: __items__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_del', { value: __del__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_clear', { value: __clear__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_get', { value: __getdefault__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_setdefault', { value: __setdefault__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_pop', { value: __pop__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_popitem', { value: __popitem__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_update', { value: __update__, enumerable: false });
Object.defineProperty(Object.prototype, 'py_values', { value: __values__, enumerable: false });
Object.defineProperty(Object.prototype, '__getitem__', { value: __dgetitem__, enumerable: false });
Object.defineProperty(Object.prototype, '__setitem__', { value: __dsetitem__, enumerable: false });
dict.__name__ = 'dict';
dict.__bases__ = [object];
function __setdoc__(docString) {
    this.__doc__ = docString;
    return this;
}
__setproperty__(Function.prototype, '__setdoc__', { value: __setdoc__, enumerable: false });
function __jsmod__(a, b) {
    if (typeof a == 'object' && '__mod__' in a) {
        return a.__mod__(b);
    }
    else if (typeof b == 'object' && '__rmod__' in b) {
        return b.__rmod__(a);
    }
    else {
        return a % b;
    }
}
;
function __mod__(a, b) {
    if (typeof a == 'object' && '__mod__' in a) {
        return a.__mod__(b);
    }
    else if (typeof b == 'object' && '__rmod__' in b) {
        return b.__rmod__(a);
    }
    else {
        return ((a % b) + b) % b;
    }
}
;
function __pow__(a, b) {
    if (typeof a == 'object' && '__pow__' in a) {
        return a.__pow__(b);
    }
    else if (typeof b == 'object' && '__rpow__' in b) {
        return b.__rpow__(a);
    }
    else {
        return Math.pow(a, b);
    }
}
;
var pow = __pow__;
function __neg__(a) {
    if (typeof a == 'object' && '__neg__' in a) {
        return a.__neg__();
    }
    else {
        return -a;
    }
}
;
function __matmul__(a, b) {
    return a.__matmul__(b);
}
;
function __mul__(a, b) {
    if (typeof a == 'object' && '__mul__' in a) {
        return a.__mul__(b);
    }
    else if (typeof b == 'object' && '__rmul__' in b) {
        return b.__rmul__(a);
    }
    else if (typeof a == 'string') {
        return a.__mul__(b);
    }
    else if (typeof b == 'string') {
        return b.__rmul__(a);
    }
    else {
        return a * b;
    }
}
;
function __truediv__(a, b) {
    if (typeof a == 'object' && '__truediv__' in a) {
        return a.__truediv__(b);
    }
    else if (typeof b == 'object' && '__rtruediv__' in b) {
        return b.__rtruediv__(a);
    }
    else if (typeof a == 'object' && '__div__' in a) {
        return a.__div__(b);
    }
    else if (typeof b == 'object' && '__rdiv__' in b) {
        return b.__rdiv__(a);
    }
    else {
        return a / b;
    }
}
;
function __floordiv__(a, b) {
    if (typeof a == 'object' && '__floordiv__' in a) {
        return a.__floordiv__(b);
    }
    else if (typeof b == 'object' && '__rfloordiv__' in b) {
        return b.__rfloordiv__(a);
    }
    else if (typeof a == 'object' && '__div__' in a) {
        return a.__div__(b);
    }
    else if (typeof b == 'object' && '__rdiv__' in b) {
        return b.__rdiv__(a);
    }
    else {
        return Math.floor(a / b);
    }
}
;
function __add__(a, b) {
    if (typeof a == 'object' && '__add__' in a) {
        return a.__add__(b);
    }
    else if (typeof b == 'object' && '__radd__' in b) {
        return b.__radd__(a);
    }
    else {
        return a + b;
    }
}
;
function __sub__(a, b) {
    if (typeof a == 'object' && '__sub__' in a) {
        return a.__sub__(b);
    }
    else if (typeof b == 'object' && '__rsub__' in b) {
        return b.__rsub__(a);
    }
    else {
        return a - b;
    }
}
;
function __lshift__(a, b) {
    if (typeof a == 'object' && '__lshift__' in a) {
        return a.__lshift__(b);
    }
    else if (typeof b == 'object' && '__rlshift__' in b) {
        return b.__rlshift__(a);
    }
    else {
        return a << b;
    }
}
;
function __rshift__(a, b) {
    if (typeof a == 'object' && '__rshift__' in a) {
        return a.__rshift__(b);
    }
    else if (typeof b == 'object' && '__rrshift__' in b) {
        return b.__rrshift__(a);
    }
    else {
        return a >> b;
    }
}
;
function __or__(a, b) {
    if (typeof a == 'object' && '__or__' in a) {
        return a.__or__(b);
    }
    else if (typeof b == 'object' && '__ror__' in b) {
        return b.__ror__(a);
    }
    else {
        return a | b;
    }
}
;
function __xor__(a, b) {
    if (typeof a == 'object' && '__xor__' in a) {
        return a.__xor__(b);
    }
    else if (typeof b == 'object' && '__rxor__' in b) {
        return b.__rxor__(a);
    }
    else {
        return a ^ b;
    }
}
;
function __and__(a, b) {
    if (typeof a == 'object' && '__and__' in a) {
        return a.__and__(b);
    }
    else if (typeof b == 'object' && '__rand__' in b) {
        return b.__rand__(a);
    }
    else {
        return a & b;
    }
}
;
function __eq__(a, b) {
    if (typeof a == 'object' && '__eq__' in a) {
        return a.__eq__(b);
    }
    else {
        return a == b;
    }
}
;
function __ne__(a, b) {
    if (typeof a == 'object' && '__ne__' in a) {
        return a.__ne__(b);
    }
    else {
        return a != b;
    }
}
;
function __lt__(a, b) {
    if (typeof a == 'object' && '__lt__' in a) {
        return a.__lt__(b);
    }
    else {
        return a < b;
    }
}
;
function __le__(a, b) {
    if (typeof a == 'object' && '__le__' in a) {
        return a.__le__(b);
    }
    else {
        return a <= b;
    }
}
;
function __gt__(a, b) {
    if (typeof a == 'object' && '__gt__' in a) {
        return a.__gt__(b);
    }
    else {
        return a > b;
    }
}
;
function __ge__(a, b) {
    if (typeof a == 'object' && '__ge__' in a) {
        return a.__ge__(b);
    }
    else {
        return a >= b;
    }
}
;
function __imatmul__(a, b) {
    if ('__imatmul__' in a) {
        return a.__imatmul__(b);
    }
    else {
        return a.__matmul__(b);
    }
}
;
function __ipow__(a, b) {
    if (typeof a == 'object' && '__pow__' in a) {
        return a.__ipow__(b);
    }
    else if (typeof a == 'object' && '__ipow__' in a) {
        return a.__pow__(b);
    }
    else if (typeof b == 'object' && '__rpow__' in b) {
        return b.__rpow__(a);
    }
    else {
        return Math.pow(a, b);
    }
}
;
function __ijsmod__(a, b) {
    if (typeof a == 'object' && '__imod__' in a) {
        return a.__ismod__(b);
    }
    else if (typeof a == 'object' && '__mod__' in a) {
        return a.__mod__(b);
    }
    else if (typeof b == 'object' && '__rpow__' in b) {
        return b.__rmod__(a);
    }
    else {
        return a % b;
    }
}
;
function __imod__(a, b) {
    if (typeof a == 'object' && '__imod__' in a) {
        return a.__imod__(b);
    }
    else if (typeof a == 'object' && '__mod__' in a) {
        return a.__mod__(b);
    }
    else if (typeof b == 'object' && '__rmod__' in b) {
        return b.__rmod__(a);
    }
    else {
        return ((a % b) + b) % b;
    }
}
;
function __imul__(a, b) {
    if (typeof a == 'object' && '__imul__' in a) {
        return a.__imul__(b);
    }
    else if (typeof a == 'object' && '__mul__' in a) {
        return a = a.__mul__(b);
    }
    else if (typeof b == 'object' && '__rmul__' in b) {
        return a = b.__rmul__(a);
    }
    else if (typeof a == 'string') {
        return a = a.__mul__(b);
    }
    else if (typeof b == 'string') {
        return a = b.__rmul__(a);
    }
    else {
        return a *= b;
    }
}
;
function __idiv__(a, b) {
    if (typeof a == 'object' && '__idiv__' in a) {
        return a.__idiv__(b);
    }
    else if (typeof a == 'object' && '__div__' in a) {
        return a = a.__div__(b);
    }
    else if (typeof b == 'object' && '__rdiv__' in b) {
        return a = b.__rdiv__(a);
    }
    else {
        return a /= b;
    }
}
;
function __iadd__(a, b) {
    if (typeof a == 'object' && '__iadd__' in a) {
        return a.__iadd__(b);
    }
    else if (typeof a == 'object' && '__add__' in a) {
        return a = a.__add__(b);
    }
    else if (typeof b == 'object' && '__radd__' in b) {
        return a = b.__radd__(a);
    }
    else {
        return a += b;
    }
}
;
function __isub__(a, b) {
    if (typeof a == 'object' && '__isub__' in a) {
        return a.__isub__(b);
    }
    else if (typeof a == 'object' && '__sub__' in a) {
        return a = a.__sub__(b);
    }
    else if (typeof b == 'object' && '__rsub__' in b) {
        return a = b.__rsub__(a);
    }
    else {
        return a -= b;
    }
}
;
function __ilshift__(a, b) {
    if (typeof a == 'object' && '__ilshift__' in a) {
        return a.__ilshift__(b);
    }
    else if (typeof a == 'object' && '__lshift__' in a) {
        return a = a.__lshift__(b);
    }
    else if (typeof b == 'object' && '__rlshift__' in b) {
        return a = b.__rlshift__(a);
    }
    else {
        return a <<= b;
    }
}
;
function __irshift__(a, b) {
    if (typeof a == 'object' && '__irshift__' in a) {
        return a.__irshift__(b);
    }
    else if (typeof a == 'object' && '__rshift__' in a) {
        return a = a.__rshift__(b);
    }
    else if (typeof b == 'object' && '__rrshift__' in b) {
        return a = b.__rrshift__(a);
    }
    else {
        return a >>= b;
    }
}
;
function __ior__(a, b) {
    if (typeof a == 'object' && '__ior__' in a) {
        return a.__ior__(b);
    }
    else if (typeof a == 'object' && '__or__' in a) {
        return a = a.__or__(b);
    }
    else if (typeof b == 'object' && '__ror__' in b) {
        return a = b.__ror__(a);
    }
    else {
        return a |= b;
    }
}
;
function __ixor__(a, b) {
    if (typeof a == 'object' && '__ixor__' in a) {
        return a.__ixor__(b);
    }
    else if (typeof a == 'object' && '__xor__' in a) {
        return a = a.__xor__(b);
    }
    else if (typeof b == 'object' && '__rxor__' in b) {
        return a = b.__rxor__(a);
    }
    else {
        return a ^= b;
    }
}
;
function __iand__(a, b) {
    if (typeof a == 'object' && '__iand__' in a) {
        return a.__iand__(b);
    }
    else if (typeof a == 'object' && '__and__' in a) {
        return a = a.__and__(b);
    }
    else if (typeof b == 'object' && '__rand__' in b) {
        return a = b.__rand__(a);
    }
    else {
        return a &= b;
    }
}
;
function __getitem__(container, key) {
    if (typeof container == 'object' && '__getitem__' in container) {
        return container.__getitem__(key);
    }
    else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
        return container[container.length + key];
    }
    else {
        return container[key];
    }
}
;
function __setitem__(container, key, value) {
    if (typeof container == 'object' && '__setitem__' in container) {
        container.__setitem__(key, value);
    }
    else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
        container[container.length + key] = value;
    }
    else {
        container[key] = value;
    }
}
;
function __getslice__(container, lower, upper, step) {
    if (typeof container == 'object' && '__getitem__' in container) {
        return container.__getitem__([lower, upper, step]);
    }
    else {
        return container.__getslice__(lower, upper, step);
    }
}
;
function __setslice__(container, lower, upper, step, value) {
    if (typeof container == 'object' && '__setitem__' in container) {
        container.__setitem__([lower, upper, step], value);
    }
    else {
        container.__setslice__(lower, upper, step, value);
    }
}
;
var BaseException = _class_('BaseException', [object], {
    __module__: __name__,
});
var Exception = _class_('Exception', [BaseException], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self) {
            var kwargs = dict();
            if (arguments.length) {
                var __ilastarg0__ = arguments.length - 1;
                if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
                    var __allkwargs0__ = arguments[__ilastarg0__--];
                    for (var __attrib0__ in __allkwargs0__) {
                        switch (__attrib0__) {
                            case 'self':
                                var self = __allkwargs0__[__attrib0__];
                                break;
                            default: kwargs[__attrib0__] = __allkwargs0__[__attrib0__];
                        }
                    }
                    delete kwargs.__kwargtrans__;
                }
                var args = tuple([].slice.apply(arguments).slice(1, __ilastarg0__ + 1));
            }
            else {
                var args = tuple();
            }
            self.__args__ = args;
            try {
                self.stack = kwargs.error.stack;
            }
            catch (__except0__) {
                self.stack = 'No stack trace available';
            }
        });
    },
    get __repr__() {
        return __get__(this, function (self) {
            if (len(self.__args__) > 1) {
                return '{}{}'.format(self.__class__.__name__, repr(tuple(self.__args__)));
            }
            else if (len(self.__args__)) {
                return '{}({})'.format(self.__class__.__name__, repr(self.__args__[0]));
            }
            else {
                return '{}()'.format(self.__class__.__name__);
            }
        });
    },
    get __str__() {
        return __get__(this, function (self) {
            if (len(self.__args__) > 1) {
                return str(tuple(self.__args__));
            }
            else if (len(self.__args__)) {
                return str(self.__args__[0]);
            }
            else {
                return '';
            }
        });
    }
});
var IterableError = _class_('IterableError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, error) {
            Exception.__init__(self, "Can't iterate over non-iterable", __kwargtrans__({ error: error }));
        });
    }
});
var StopIteration = _class_('StopIteration', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, error) {
            Exception.__init__(self, 'Iterator exhausted', __kwargtrans__({ error: error }));
        });
    }
});
var ValueError = _class_('ValueError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, message, error) {
            Exception.__init__(self, message, __kwargtrans__({ error: error }));
        });
    }
});
var KeyError = _class_('KeyError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, message, error) {
            Exception.__init__(self, message, __kwargtrans__({ error: error }));
        });
    }
});
var AssertionError = _class_('AssertionError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, message, error) {
            if (message) {
                Exception.__init__(self, message, __kwargtrans__({ error: error }));
            }
            else {
                Exception.__init__(self, __kwargtrans__({ error: error }));
            }
        });
    }
});
var NotImplementedError = _class_('NotImplementedError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, message, error) {
            Exception.__init__(self, message, __kwargtrans__({ error: error }));
        });
    }
});
var IndexError = _class_('IndexError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, message, error) {
            Exception.__init__(self, message, __kwargtrans__({ error: error }));
        });
    }
});
var AttributeError = _class_('AttributeError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, message, error) {
            Exception.__init__(self, message, __kwargtrans__({ error: error }));
        });
    }
});
var py_TypeError = _class_('py_TypeError', [Exception], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self, message, error) {
            Exception.__init__(self, message, __kwargtrans__({ error: error }));
        });
    }
});
var Warning = _class_('Warning', [Exception], {
    __module__: __name__,
});
var UserWarning = _class_('UserWarning', [Warning], {
    __module__: __name__,
});
var DeprecationWarning = _class_('DeprecationWarning', [Warning], {
    __module__: __name__,
});
var RuntimeWarning = _class_('RuntimeWarning', [Warning], {
    __module__: __name__,
});
var __sort__ = function (iterable, key, reverse) {
    if (arguments.length) {
        var __ilastarg0__ = arguments.length - 1;
        if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
            var __allkwargs0__ = arguments[__ilastarg0__--];
            for (var __attrib0__ in __allkwargs0__) {
                switch (__attrib0__) {
                    case 'iterable':
                        var iterable = __allkwargs0__[__attrib0__];
                        break;
                    case 'key':
                        var key = __allkwargs0__[__attrib0__];
                        break;
                    case 'reverse':
                        var reverse = __allkwargs0__[__attrib0__];
                        break;
                }
            }
        }
    }
    else {
    }
    if (typeof key == 'undefined' || (key != null && key.hasOwnProperty("__kwargtrans__"))) {
        ;
        var key = null;
    }
    ;
    if (typeof reverse == 'undefined' || (reverse != null && reverse.hasOwnProperty("__kwargtrans__"))) {
        ;
        var reverse = false;
    }
    ;
    if (key) {
        iterable.sort((function __lambda__(a, b) {
            if (arguments.length) {
                var __ilastarg0__ = arguments.length - 1;
                if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
                    var __allkwargs0__ = arguments[__ilastarg0__--];
                    for (var __attrib0__ in __allkwargs0__) {
                        switch (__attrib0__) {
                            case 'a':
                                var a = __allkwargs0__[__attrib0__];
                                break;
                            case 'b':
                                var b = __allkwargs0__[__attrib0__];
                                break;
                        }
                    }
                }
            }
            else {
            }
            return (key(a) > key(b) ? 1 : -(1));
        }));
    }
    else {
        iterable.sort();
    }
    if (reverse) {
        iterable.reverse();
    }
};
var sorted = function (iterable, key, reverse) {
    if (arguments.length) {
        var __ilastarg0__ = arguments.length - 1;
        if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
            var __allkwargs0__ = arguments[__ilastarg0__--];
            for (var __attrib0__ in __allkwargs0__) {
                switch (__attrib0__) {
                    case 'iterable':
                        var iterable = __allkwargs0__[__attrib0__];
                        break;
                    case 'key':
                        var key = __allkwargs0__[__attrib0__];
                        break;
                    case 'reverse':
                        var reverse = __allkwargs0__[__attrib0__];
                        break;
                }
            }
        }
    }
    else {
    }
    if (typeof key == 'undefined' || (key != null && key.hasOwnProperty("__kwargtrans__"))) {
        ;
        var key = null;
    }
    ;
    if (typeof reverse == 'undefined' || (reverse != null && reverse.hasOwnProperty("__kwargtrans__"))) {
        ;
        var reverse = false;
    }
    ;
    if (py_typeof(iterable) == dict) {
        var result = copy(iterable.py_keys());
    }
    else {
        var result = copy(iterable);
    }
    __sort__(result, key, reverse);
    return result;
};
var map = function (func, iterable) {
    return (function () {
        var __accu0__ = [];
        for (var item of iterable) {
            __accu0__.append(func(item));
        }
        return __accu0__;
    })();
};
var filter = function (func, iterable) {
    if (func == null) {
        var func = bool;
    }
    return (function () {
        var __accu0__ = [];
        for (var item of iterable) {
            if (func(item)) {
                __accu0__.append(item);
            }
        }
        return __accu0__;
    })();
};
var divmod = function (n, d) {
    return tuple([Math.floor(n / d), __mod__(n, d)]);
};
var __Terminal__ = _class_('__Terminal__', [object], {
    __module__: __name__,
    get __init__() {
        return __get__(this, function (self) {
            self.buffer = '';
            try {
                self.element = document.getElementById('__terminal__');
            }
            catch (__except0__) {
                self.element = null;
            }
            if (self.element) {
                self.element.style.overflowX = 'auto';
                self.element.style.boxSizing = 'border-box';
                self.element.style.padding = '5px';
                self.element.innerHTML = '_';
            }
        });
    },
    get print() {
        return __get__(this, function (self) {
            if (arguments.length) {
                var __ilastarg0__ = arguments.length - 1;
                if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
                    var __allkwargs0__ = arguments[__ilastarg0__--];
                    for (var __attrib0__ in __allkwargs0__) {
                        switch (__attrib0__) {
                            case 'self':
                                var self = __allkwargs0__[__attrib0__];
                                break;
                            case 'sep':
                                var sep = __allkwargs0__[__attrib0__];
                                break;
                            case 'end':
                                var end = __allkwargs0__[__attrib0__];
                                break;
                        }
                    }
                }
                var args = tuple([].slice.apply(arguments).slice(1, __ilastarg0__ + 1));
            }
            else {
                var args = tuple();
            }
            var sep = ' ';
            var end = '\n';
            self.buffer = '{}{}{}'.format(self.buffer, sep.join((function () {
                var __accu0__ = [];
                for (var arg of args) {
                    __accu0__.append(str(arg));
                }
                return __accu0__;
            })()), end).__getslice__(-(4096), null, 1);
            if (self.element) {
                self.element.innerHTML = self.buffer.py_replace('\n', '<br>').py_replace(' ', '&nbsp');
                self.element.scrollTop = self.element.scrollHeight;
            }
            else {
                console.log(sep.join((function () {
                    var __accu0__ = [];
                    for (var arg of args) {
                        __accu0__.append(str(arg));
                    }
                    return __accu0__;
                })()));
            }
        });
    },
    get input() {
        return __get__(this, function (self, question) {
            if (arguments.length) {
                var __ilastarg0__ = arguments.length - 1;
                if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
                    var __allkwargs0__ = arguments[__ilastarg0__--];
                    for (var __attrib0__ in __allkwargs0__) {
                        switch (__attrib0__) {
                            case 'self':
                                var self = __allkwargs0__[__attrib0__];
                                break;
                            case 'question':
                                var question = __allkwargs0__[__attrib0__];
                                break;
                        }
                    }
                }
            }
            else {
            }
            self.print('{}'.format(question), __kwargtrans__({ end: '' }));
            var answer = window.prompt('\n'.join(self.buffer.py_split('\n').__getslice__(-(8), null, 1)));
            self.print(answer);
            return answer;
        });
    }
});
var __terminal__ = __Terminal__();
var print = __terminal__.print;
var input = __terminal__.input;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./client/components/Loading/style.css":
/*!***********************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./client/components/Loading/style.css ***!
  \***********************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.container.is-loading {
    min-height: 100px;
}

.loading {
    fill: var(--jp-ui-font-color1);
    stop-color: var(--jp-ui-font-color1);
    color: var(--jp-ui-font-color1);
}

.loading svg stop {
    stop-color: var(--jp-ui-font-color1);
}

.loading svg circle {
    fill: var(--jp-ui-font-color1);
}
`, "",{"version":3,"sources":["webpack://./client/components/Loading/style.css"],"names":[],"mappings":"AAAA;IACI,iBAAiB;AACrB;;AAEA;IACI,8BAA8B;IAC9B,oCAAoC;IACpC,+BAA+B;AACnC;;AAEA;IACI,oCAAoC;AACxC;;AAEA;IACI,8BAA8B;AAClC","sourcesContent":[".container.is-loading {\n    min-height: 100px;\n}\n\n.loading {\n    fill: var(--jp-ui-font-color1);\n    stop-color: var(--jp-ui-font-color1);\n    color: var(--jp-ui-font-color1);\n}\n\n.loading svg stop {\n    stop-color: var(--jp-ui-font-color1);\n}\n\n.loading svg circle {\n    fill: var(--jp-ui-font-color1);\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./client/jupyter/style.css":
/*!************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./client/jupyter/style.css ***!
  \************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/* Otherwise, when detaching the widget and height is only set via min-height, the view is collapsed */
.lm-Widget.lm-Panel.jp-OutputArea-child.jp-OutputArea-executeResult:has(.pret-view) {
    height: 100%;
}
`, "",{"version":3,"sources":["webpack://./client/jupyter/style.css"],"names":[],"mappings":"AAAA,sGAAsG;AACtG;IACI,YAAY;AAChB","sourcesContent":["/* Otherwise, when detaching the widget and height is only set via min-height, the view is collapsed */\n.lm-Widget.lm-Panel.jp-OutputArea-child.jp-OutputArea-executeResult:has(.pret-view) {\n    height: 100%;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ })

}]);
//# sourceMappingURL=client_jupyter_plugin_tsx.7946f377cd64f62f5840.js.map