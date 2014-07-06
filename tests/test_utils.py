from rest_toolkit.utils import merge


class Test_merge(object):
    def test_disjunct_dictionaries(self):
        assert merge({'foo': 'bar'}, {'buz': True}) == {'foo': 'bar', 'buz': True}

    def test_overlap(self):
        assert merge({'foo': 'bar'}, {'foo': True}) == {'foo': True}

    def test_key_only_in_base(self):
        assert merge({'foo': 'bar'}, {}) == {'foo': 'bar'}

    def test_key_only_in_overlay(self):
        assert merge({}, {'foo': 'bar'}) == {'foo': 'bar'}

    def test_recurse(self):
        assert merge({'obj': {}}, {'obj': {'foo': 'bar'}}) == {'obj': {'foo': 'bar'}}

    def test_do_not_modify_input(self):
        base = {'foo': 'bar'}
        overlay = {'buz': True}
        merge(base, overlay)
        assert base == {'foo': 'bar'}
        assert overlay == {'buz': True}
