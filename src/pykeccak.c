/*
 * Python wrapper around Keccak core.
 *
 * Copyright (c) 2013 Marko Kreen
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include "keccak.h"

#if PY_MAJOR_VERSION >= 3
#define PyString_FromString(s) PyUnicode_FromString(s)
#endif

#define SPONGE_MODULE	"keccak"
#define SPONGE_CLASS	"KeccakSponge"
#define SPONGE_NAME	"Keccak1600"
#define MODINIT2	initkeccak
#define MODINIT3	PyInit_keccak

static const char mod_doc[] =
"Implements Sponge API for Keccak-f1600.";

static const char Sponge_doc[] =
SPONGE_CLASS "(capacity) - Initializes Sponge object with given capacity in bits.";

/*
 * Main state object.
 */

typedef struct {
	PyObject_HEAD
	struct KeccakContext md;
} SpongeObject;

static SpongeObject *alloc_sponge(void);
static bool get_buffer(PyObject *obj, Py_buffer *buf);


static const char Sponge_new_doc[] =
SPONGE_CLASS "(capacity_bits) - Create new state object with given capacity.";

static int Sponge_init(PyObject *obj, PyObject *args, PyObject *kws)
{
	SpongeObject *self = (SpongeObject *)obj;
	unsigned int cap;
	static char *kwlist[] = { "capacity", 0 };

        if (!PyArg_ParseTupleAndKeywords(args, kws, "I", kwlist, &cap))
                return -1;

        if (keccak_init(&self->md, cap) != 1) {
		PyErr_SetString(PyExc_ValueError, "Invalid capacity");
		return -1;
	}

	return 0;
}

static void Sponge_dealloc(PyObject *obj)
{
	SpongeObject *self = (SpongeObject *)obj;
	memset(&self->md, 0, sizeof(self->md));
        PyObject_Del(obj);
}

static const char Sponge_copy_doc[] =
"copy() - Copy current state to new object.";

static PyObject *Sponge_copy(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;
	SpongeObject *res;

        res = alloc_sponge();
	memcpy(&res->md, &self->md, sizeof(res->md));

	return (PyObject *)res;
}

static bool get_buffer(PyObject *obj, Py_buffer *buf)
{
	if (PyUnicode_Check(obj)) {
		PyErr_SetString(PyExc_TypeError,
				"Unicode-objects must be encoded before hashing");
		return false;
	}
	if (!PyObject_CheckBuffer(obj)) {
		PyErr_SetString(PyExc_TypeError,
				"object supporting the buffer API required");
		return false;
	}
	if (PyObject_GetBuffer(obj, buf, PyBUF_SIMPLE) == -1) {
		return false;
	}
	if (buf->ndim > 1) {
		PyErr_SetString(PyExc_BufferError,
				"Buffer must be single dimension");
		PyBuffer_Release(buf);
		return false;
	}
	return true;
}

static const char Sponge_absorb_doc[] =
"absorb(data) - XOR data into state.";

static PyObject *Sponge_absorb(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;
	PyObject *dataobj;
	Py_buffer buf;

	if (!PyArg_ParseTuple(args, "O", &dataobj))
		return NULL;
	if (!get_buffer(dataobj, &buf))
		return NULL;

	keccak_absorb(&self->md, buf.buf, buf.len);

	PyBuffer_Release(&buf);

	Py_INCREF(Py_None);
	return Py_None;
}

static const char Sponge_pad_doc[] =
"pad(suffix) - Add padding and permute state.\n"
"\n"
"The suffix is added into state, then also final bit is flipped.\n"
"So to get original simple 10*1 padding given in the Keccak SHA3 proposal,\n"
"the suffix needs to be '\\\\x01'.\n"
"\n"
"If padding is suffix is empty, then final bit is not flipped, to support\n"
"case when initial data for encryption is added without padding - which\n"
"is bad style.";

static PyObject *Sponge_pad(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;
	PyObject *dataobj;
	Py_buffer buf;

	if (!PyArg_ParseTuple(args, "O", &dataobj))
		return NULL;
	if (!get_buffer(dataobj, &buf))
		return NULL;

	keccak_pad(&self->md, buf.buf, buf.len);

	PyBuffer_Release(&buf);

	Py_INCREF(Py_None);
	return Py_None;
}

static const char Sponge_squeeze_doc[] =
"squeeze(nbytes) - extract given number of bytes from state.";

static PyObject *Sponge_squeeze(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;
	unsigned int nbytes;
	PyObject *res;
	void *resdata;

        if (!PyArg_ParseTuple(args, "I", &nbytes))
                return NULL;

	/* allocate result object */
	res = PyBytes_FromStringAndSize(NULL, nbytes);
	if (!res)
		return NULL;

	/* get internal buffer */
	resdata = PyBytes_AsString(res);
	if (!resdata) {
		Py_CLEAR(res);
		return NULL;
	}

	keccak_squeeze(&self->md, resdata, nbytes);

	return res;
}

static const char Sponge_squeeze_xor_doc[] =
"squeeze_xor(data) - return data XOR-ed with state.";

static PyObject *Sponge_squeeze_xor(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;
	PyObject *res;
	PyObject *dataobj;
	void *resdata;
	Py_buffer buf;

	if (!PyArg_ParseTuple(args, "O", &dataobj))
		return NULL;
	if (!get_buffer(dataobj, &buf))
		return NULL;

	/* allocate result object */
	res = PyBytes_FromStringAndSize(NULL, buf.len);
	if (!res) {
		PyBuffer_Release(&buf);
		return NULL;
	}

	/* get internal buffer */
	resdata = PyBytes_AsString(res);
	if (!resdata) {
		PyBuffer_Release(&buf);
		Py_CLEAR(res);
		return NULL;
	}

	keccak_squeeze_xor(&self->md, resdata, buf.buf, buf.len);

	PyBuffer_Release(&buf);

	return res;
}

static const char Sponge_encrypt_doc[] =
"encrypt(data) - return data XOR-ed into state.\n"
"\n"
"The state should already absorbed and permuted before\n"
"encrypting starts.  This means .absorb(key) + .pad()\n"
"should be called.";

static PyObject *Sponge_encrypt(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;
	PyObject *res;
	PyObject *dataobj;
	void *resdata;
	Py_buffer buf;

	if (!PyArg_ParseTuple(args, "O", &dataobj))
		return NULL;
	if (!get_buffer(dataobj, &buf))
		return NULL;

	/* allocate result object */
	res = PyBytes_FromStringAndSize(NULL, buf.len);
	if (!res) {
		PyBuffer_Release(&buf);
		return NULL;
	}

	/* get internal buffer */
	resdata = PyBytes_AsString(res);
	if (!resdata) {
		PyBuffer_Release(&buf);
		Py_CLEAR(res);
		return NULL;
	}

	keccak_encrypt(&self->md, resdata, buf.buf, buf.len);

	PyBuffer_Release(&buf);

	return res;
}

static const char Sponge_decrypt_doc[] =
"decrypt(enc_data) - return enc_data XOR-ed with state.\n"
"\n"
"This is reverse of .encrypt() - it assumes enc_data\n"
"was created by XOR-ing current state with cleartext.\n"
"This function reverses it.";

static PyObject *Sponge_decrypt(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;
	PyObject *res;
	PyObject *dataobj;
	void *resdata;
	Py_buffer buf;

	if (!PyArg_ParseTuple(args, "O", &dataobj))
		return NULL;
	if (!get_buffer(dataobj, &buf))
		return NULL;

	/* allocate result object */
	res = PyBytes_FromStringAndSize(NULL, buf.len);
	if (!res) {
		PyBuffer_Release(&buf);
		return NULL;
	}

	/* get internal buffer */
	resdata = PyBytes_AsString(res);
	if (!resdata) {
		PyBuffer_Release(&buf);
		Py_CLEAR(res);
		return NULL;
	}

	keccak_decrypt(&self->md, resdata, buf.buf, buf.len);

	PyBuffer_Release(&buf);

	return res;
}

static const char Sponge_rewind_doc[] =
"rewind() - move internal position to start of state.\n"
"\n"
"Useful for PRNG/duplex modes.  In fact, it should not\n"
"be touched at all in other modes.";

static PyObject *Sponge_rewind(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;

	keccak_rewind(&self->md);

	Py_INCREF(Py_None);
	return Py_None;
}

static const char Sponge_forget_doc[] =
"forget() - clear internal state, except capacity.";

static PyObject *Sponge_forget(PyObject *obj, PyObject *args)
{
	SpongeObject *self = (SpongeObject *)obj;

	keccak_forget(&self->md);

	Py_INCREF(Py_None);
	return Py_None;
}

/*
 * getters
 */

static PyObject *Sponge_get_name(PyObject *obj, void *xtra)
{
	SpongeObject *self = (SpongeObject *)obj;
	int cap = 1600 - self->md.rbytes * 8;
	char buf[128];

	snprintf(buf, sizeof(buf), "%s-%d", SPONGE_NAME, cap);
	return PyString_FromString(buf);
}

static PyObject *Sponge_get_rate(PyObject *obj, void *xtra)
{
	SpongeObject *self = (SpongeObject *)obj;
	return PyLong_FromLong(self->md.rbytes * 8);
}

static PyObject *Sponge_get_capacity(PyObject *obj, void *xtra)
{
	SpongeObject *self = (SpongeObject *)obj;
	return PyLong_FromLong(1600 - self->md.rbytes * 8);
}

static PyObject *Sponge_get_pos(PyObject *obj, void *xtra)
{
	SpongeObject *self = (SpongeObject *)obj;
	return PyLong_FromLong(self->md.pos);
}

static PyObject *Sponge_get_rbytes(PyObject *obj, void *xtra)
{
	SpongeObject *self = (SpongeObject *)obj;
	return PyLong_FromLong(self->md.rbytes);
}

/*
 * Class initialization
 */

static PyMethodDef Sponge_methods[] = {
	{ "copy", Sponge_copy, METH_NOARGS, Sponge_copy_doc},
	{ "absorb", Sponge_absorb, METH_VARARGS, Sponge_absorb_doc },
	{ "squeeze", Sponge_squeeze, METH_VARARGS, Sponge_squeeze_doc },
	{ "squeeze_xor", Sponge_squeeze_xor, METH_VARARGS, Sponge_squeeze_xor_doc },
	{ "encrypt", Sponge_encrypt, METH_VARARGS, Sponge_encrypt_doc },
	{ "decrypt", Sponge_decrypt, METH_VARARGS, Sponge_decrypt_doc },
	{ "pad", Sponge_pad, METH_VARARGS, Sponge_pad_doc },
	{ "rewind", Sponge_rewind, METH_NOARGS, Sponge_rewind_doc },
	{ "forget", Sponge_forget, METH_NOARGS, Sponge_forget_doc },
	{ NULL }
};

static PyGetSetDef Sponge_getters[] = {
	/* name, get, set, doc, closure */
	{ "name", Sponge_get_name, NULL, "Sponge name", NULL },
	{ "rate", Sponge_get_rate, NULL, "Sponge rate in bits", NULL },
	{ "capacity", Sponge_get_capacity, NULL, "Sponge capacity in bits", NULL },
	{ "rbytes", Sponge_get_rbytes, NULL, "Current position in bytes", NULL },
	{ "pos", Sponge_get_pos, NULL, "Current position in bytes", NULL },
	{ NULL }
};

static PyTypeObject SpongeType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	SPONGE_MODULE "." SPONGE_CLASS,	/* tp_name */
	sizeof(SpongeType),	/* tp_size */
	0,			/* tp_itemsize */
	Sponge_dealloc,	/* tp_dealloc */
	0,			/* tp_print */
	0,			/* tp_getattr */
	0,			/* tp_setattr */
	0,			/* tp_reserved */
	0,			/* tp_repr */
	0,			/* tp_as_number */
	0,			/* tp_as_sequence */
	0,			/* tp_as_mapping */
	PyObject_HashNotImplemented, /* tp_hash */
	0,			/* tp_call */
	0,			/* tp_str */
	0,			/* tp_getattro */
	0,			/* tp_setattro */
	0,			/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,	/* tp_flags */
	Sponge_doc,		/* tp_doc */
	0,			/* tp_traverse */
	0,			/* tp_clear */
	0,			/* tp_richcompare */
	0,			/* tp_weaklistoffset */
	0,			/* tp_iter */
	0,			/* tp_iternext */
	Sponge_methods,	/* tp_methods */
	NULL,			/* tp_members */
	Sponge_getters,	/* tp_getset */
	0,			/* tp_base */
	0,			/* tp_dict */
	0,			/* tp_descr_get */
	0,			/* tp_descr_set */
	0,			/* tp_dictoffset */
	Sponge_init,	/* tp_init */
	PyType_GenericAlloc,	/* tp_alloc */
	PyType_GenericNew,	/* tp_new */
	PyObject_Del,		/* tp_free */
};

static SpongeObject *alloc_sponge(void)
{
	return PyObject_New(SpongeObject, &SpongeType);
}

/*
 * Module initialization
 */

/* common module init */
static PyObject *mod_init(PyObject *mod)
{
	PyObject *name, *all;

	Py_TYPE(&SpongeType) = &PyType_Type;
	if (PyType_Ready(&SpongeType) != 0)
		return NULL;

	Py_INCREF((PyObject *)&SpongeType);
	if (PyModule_AddObject(mod, SPONGE_CLASS, (PyObject *)&SpongeType) != 0)
		return NULL;


	name = PyString_FromString(SPONGE_CLASS);
	if (name) {
		all = PyTuple_Pack(1, name);
		if (all)
			PyModule_AddObject(mod, "__all__", all);
		else
			Py_CLEAR(name);
	}

	return mod;
}

/*
 * Py2/3 specific parts.
 */

#if PY_MAJOR_VERSION < 3

PyMODINIT_FUNC MODINIT2(void)
{
	PyObject *m;

	m = Py_InitModule(SPONGE_MODULE, NULL);
	if (m == NULL)
		return;

	PyModule_AddStringConstant(m, "__doc__", mod_doc);

	mod_init(m);
}

#else

static struct PyModuleDef modInfo = {
	PyModuleDef_HEAD_INIT,	/* m_base */
	SPONGE_MODULE,		/* m_name */
	mod_doc,		/* m_doc */
	-1,			/* m_size */
	NULL,			/* m_methods */
	NULL,			/* m_reload */
	NULL,			/* m_traverse */
	NULL,			/* m_clear */
	NULL			/* m_free */
};

PyMODINIT_FUNC MODINIT3(void)
{
	PyObject *m;

	m = PyModule_Create(&modInfo);
	if (!m)
		return NULL;

	return mod_init(m);
}

#endif

