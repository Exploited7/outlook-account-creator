function encrypt(r, t, e) {
    if (o = PackageNewPwdOnly(r), null == o || "undefined" == typeof o) return o;
    if (void 0 !== e && void 0 !== parseRSAKeyFromString) var a = parseRSAKeyFromString(e);
    return RSAEncrypt(o, a, t)
}

function PackagePwdOnly(r) {
    var t = [],
        e = 0;
    t[e++] = 1, t[e++] = 1, t[e++] = 0, t[e++] = 0;
    var a, n = r.length;
    for (t[e++] = n, a = 0; n > a; a++) t[e++] = 127 & r.charCodeAt(a);
    return t
}

function RSAEncrypt(r, t, e) {
    t || (t = {
        n: []
    });
    for (var a = [], n = 2 * t.n.size - 42, o = 0; o < r.length; o += n) {
        var i;
        if (o + n >= r.length)(i = RSAEncryptBlock(r.slice(o), t, e)) && (a = i.concat(a));
        else(i = RSAEncryptBlock(r.slice(o, o + n), t, e)) && (a = i.concat(a))
    }
    return byteArrayToBase64(a)
}

function RSAEncryptBlock(r, t, e) {
    var a = t.n,
        n = t.e,
        o = r.length,
        i = 2 * a.size;
    if (o + 42 > i) return null;
    applyPKCSv2Padding(r, i, e);
    var u = byteArrayToMP(r = r.reverse()),
        f = modularExp(u, n, a);
    f.size = a.size;
    var l = mpToByteArray(f);
    return l.reverse()
}

function parseRSAKeyFromString(r) {
    var t = r.indexOf(";");
    if (0 > t) return null;
    var e = r.substr(0, t),
        a = r.substr(t + 1),
        n = e.indexOf("=");
    if (0 > n) return null;
    var o = e.substr(n + 1);
    if (0 > (n = a.indexOf("="))) return null;
    var i = a.substr(n + 1),
        u = new Object;
    return u.n = hexStringToMP(i), u.e = parseInt(o, 16), u
}

function applyPKCSv2Padding(r, t, e) {
    var a, n = t - r.length - 40 - 2,
        o = [];
    for (a = 0; n > a; a++) o[a] = 0;
    o[n] = 1;
    var i = [218, 57, 163, 238, 94, 107, 75, 13, 50, 85, 191, 239, 149, 96, 24, 144, 175, 216, 7, 9].concat(o, r),
        u = [];
    for (a = 0; 20 > a; a++) u[a] = Math.floor(256 * Math.random());
    var f = XORarrays(i, MGF(u = SHA1(u.concat(e)), t - 21)),
        l = XORarrays(u, MGF(f, 20)),
        d = [];
    for (d[0] = 0, d = d.concat(l, f), a = 0; a < d.length; a++) r[a] = d[a]
}

function SHA1(r) {
    var t, e = r.slice(0);
    PadSHA1Input(e);
    var a = {
        A: 1732584193,
        B: 4023233417,
        C: 2562383102,
        D: 271733878,
        E: 3285377520
    };
    for (t = 0; t < e.length; t += 64) SHA1RoundFunction(a, e, t);
    var n = [];
    return wordToBytes(a.A, n, 0), wordToBytes(a.B, n, 4), wordToBytes(a.C, n, 8), wordToBytes(a.D, n, 12), wordToBytes(a.E, n, 16), n
}

function PadSHA1Input(r) {
    var t, e = r.length,
        a = e,
        n = e % 64,
        o = 55 > n ? 56 : 120;
    for (r[a++] = 128, t = n + 1; o > t; t++) r[a++] = 0;
    var i = 8 * e;
    for (t = 1; 8 > t; t++) r[a + 8 - t] = 255 & i, i >>>= 8
}

function SHA1RoundFunction(r, t, e) {
    var a, n, o, i, u = [],
        f = r.A,
        l = r.B,
        d = r.C,
        c = r.D,
        s = r.E;
    for (n = 0, o = e; 16 > n; n++, o += 4) u[n] = t[o] << 24 | t[o + 1] << 16 | t[o + 2] << 8 | t[o + 3] << 0;
    for (n = 16; 80 > n; n++) u[n] = rotateLeft(u[n - 3] ^ u[n - 8] ^ u[n - 14] ^ u[n - 16], 1);
    for (a = 0; 20 > a; a++) i = rotateLeft(f, 5) + (l & d | ~l & c) + s + u[a] + 1518500249 & 4294967295, s = c, c = d, d = rotateLeft(l, 30), l = f, f = i;
    for (a = 20; 40 > a; a++) i = rotateLeft(f, 5) + (l ^ d ^ c) + s + u[a] + 1859775393 & 4294967295, s = c, c = d, d = rotateLeft(l, 30), l = f, f = i;
    for (a = 40; 60 > a; a++) i = rotateLeft(f, 5) + (l & d | l & c | d & c) + s + u[a] + 2400959708 & 4294967295, s = c, c = d, d = rotateLeft(l, 30), l = f, f = i;
    for (a = 60; 80 > a; a++) i = rotateLeft(f, 5) + (l ^ d ^ c) + s + u[a] + 3395469782 & 4294967295, s = c, c = d, d = rotateLeft(l, 30), l = f, f = i;
    r.A = r.A + f & 4294967295, r.B = r.B + l & 4294967295, r.C = r.C + d & 4294967295, r.D = r.D + c & 4294967295, r.E = r.E + s & 4294967295
}

function wordToBytes(r, t, e) {
    var a;
    for (a = 3; a >= 0; a--) t[e + a] = 255 & r, r >>>= 8
}

function rotateLeft(r, t) {
    return (r & (1 << 32 - t) - 1) << t | r >>> 32 - t
}

function hexStringToMP(r) {
    var t, e, a = Math.ceil(r.length / 4),
        n = new JSMPnumber;
    for (n.size = a, t = 0; a > t; t++) e = r.substr(4 * t, 4), n.data[a - 1 - t] = parseInt(e, 16);
    return n
}

function MGF(r, t) {
    if (t > 4096) return null;
    var e = r.slice(0),
        a = e.length;
    e[a++] = 0, e[a++] = 0, e[a++] = 0, e[a] = 0;
    for (var n = 0, o = []; o.length < t;) e[a] = n++, o = o.concat(SHA1(e));
    return o.slice(0, t)
}

function XORarrays(r, t) {
    if (r.length != t.length) return null;
    for (var e = [], a = r.length, n = 0; a > n; n++) e[n] = r[n] ^ t[n];
    return e
}

function byteArrayToBase64(r) {
    var t, e, a = r.length,
        n = "";
    for (t = a - 3; t >= 0; t -= 3) n += base64Encode(e = r[t] | r[t + 1] << 8 | r[t + 2] << 16, 4);
    var o = a % 3;
    for (e = 0, t += 2; t >= 0; t--) e = e << 8 | r[t];
    return 1 == o ? n = n + base64Encode(e << 16, 2) + "==" : 2 == o && (n = n + base64Encode(e << 8, 3) + "="), n
}

function byteArrayToMP(r) {
    var t = new JSMPnumber,
        e = 0,
        a = r.length,
        n = a >> 1;
    for (e = 0; n > e; e++) t.data[e] = r[2 * e] + (r[1 + 2 * e] << 8);
    return a % 2 && (t.data[e++] = r[a - 1]), t.size = e, t
}

function mpToByteArray(r) {
    var t = [],
        e = 0,
        a = r.size;
    for (e = 0; a > e; e++) {
        t[2 * e] = 255 & r.data[e];
        var n = r.data[e] >>> 8;
        t[2 * e + 1] = n
    }
    return t
}

function modularExp(r, t, e) {
    for (var a = [], n = 0; t > 0;) a[n] = 1 & t, t >>>= 1, n++;
    for (var o = duplicateMP(r), i = n - 2; i >= 0; i--) o = modularMultiply(o, o, e), 1 == a[i] && (o = modularMultiply(o, r, e));
    return o
}

function JSMPnumber() {
    this.size = 1, this.data = [], this.data[0] = 0
}

function duplicateMP(r) {
    var t = new JSMPnumber;
    return t.size = r.size, t.data = r.data.slice(0), t
}

function modularExp(r, t, e) {
    for (var a = [], n = 0; t > 0;) a[n] = 1 & t, t >>>= 1, n++;
    for (var o = duplicateMP(r), i = n - 2; i >= 0; i--) o = modularMultiply(o, o, e), 1 == a[i] && (o = modularMultiply(o, r, e));
    return o
}

function modularMultiply(r, t, e) {
    return divideMP(multiplyMP(r, t), e).r
}

function multiplyMP(r, t) {
    var e, a, n = new JSMPnumber;
    for (n.size = r.size + t.size, e = 0; e < n.size; e++) n.data[e] = 0;
    var o = r.data,
        i = t.data,
        u = n.data;
    if (r == t) {
        for (e = 0; e < r.size; e++) u[2 * e] += o[e] * o[e];
        for (e = 1; e < r.size; e++)
            for (a = 0; e > a; a++) u[e + a] += 2 * o[e] * o[a]
    } else
        for (e = 0; e < r.size; e++)
            for (a = 0; a < t.size; a++) u[e + a] += o[e] * i[a];
    return normalizeJSMP(n), n
}

function normalizeJSMP(r) {
    var t, e, a, n;
    for (a = r.size, e = 0, t = 0; a > t; t++) n = r.data[t], n += e, n -= 65536 * (e = Math.floor(n / 65536)), r.data[t] = n
}

function removeLeadingZeroes(r) {
    for (var t = r.size - 1; t > 0 && 0 == r.data[t--];) r.size--
}

function divideMP(r, t) {
    var e = r.size,
        a = t.size,
        n = t.data[a - 1],
        o = t.data[a - 1] + t.data[a - 2] / 65536,
        i = new JSMPnumber;
    i.size = e - a + 1, r.data[e] = 0;
    for (var u = e - 1; u >= a - 1; u--) {
        var f = u - a + 1,
            l = Math.floor((65536 * r.data[u + 1] + r.data[u]) / o);
        if (l > 0) {
            var d = multiplyAndSubtract(r, l, t, f);
            for (0 > d && multiplyAndSubtract(r, --l, t, f); d > 0 && r.data[u] >= n;)(d = multiplyAndSubtract(r, 1, t, f)) > 0 && l++
        }
        i.data[f] = l
    }
    return removeLeadingZeroes(r), {
        q: i,
        r: r
    }
}

function multiplyAndSubtract(r, t, e, a) {
    var n, o = r.data.slice(0),
        i = 0,
        u = r.data;
    for (n = 0; n < e.size; n++) {
        var f = i + e.data[n] * t;
        (f -= 65536 * (i = f >>> 16)) > u[n + a] ? (u[n + a] += 65536 - f, i++) : u[n + a] -= f
    }
    return i > 0 && (u[n + a] -= i), u[n + a] < 0 ? (r.data = o.slice(0), -1) : 1
}

function base64Encode(r, t) {
    var e, a = "";
    for (e = t; 4 > e; e++) r >>= 6;
    for (e = 0; t > e; e++) a = mapByteToBase64(63 & r) + a, r >>= 6;
    return a
}

function mapByteToBase64(r) {
    return r >= 0 && 26 > r ? String.fromCharCode(65 + r) : r >= 26 && 52 > r ? String.fromCharCode(97 + r - 26) : r >= 52 && 62 > r ? String.fromCharCode(48 + r - 52) : 62 == r ? "+" : "/"
}

function PackageNewPwdOnly(r) {
    var t = [],
        e = 0;
    t[e++] = 1, t[e++] = 1;
    var a, n = r.length;
    for (t[e++] = n, a = 0; n > a; a++) t[e++] = 127 & r.charCodeAt(a);
    return t[e++] = 0, t[e++] = 0, t
}