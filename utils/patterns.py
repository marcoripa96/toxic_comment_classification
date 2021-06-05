regex_patterns = {
    ' fuck ':
        [
            '(f)(u|[^a-z0-9 ])(c|[^a-z0-9 ])(k|[^a-z0-9 ])([^ ])*',
            ' f[!@#\$%\^\&\*]*u[!@#\$%\^&\*]*k', 'f u u c',
            '(f)(c|[^a-z ])(u|[^a-z ])(k)', r'f\*',
            'feck ', ' fux ', 'f\*\*', 
            'f\-ing', 'f\.u\.', 'f###', ' fu ', 'f@ck', 'f u c k', 'f uck', 'f ck'
        ],
    ' bitch ':
        [
            'b[w]*i[t]*ch', 'b!tch',
            'bi\+ch', 'b!\+ch',
            'biatch', 'bi\*\*h', 'bytch', 'b i t c h'
        ],
    ' mother fucker ':
        [
            ' motha ', ' motha f', ' mother f', 'motherucker',
        ],
    ' pussy ':
        [
            'pussy[^c]', 'pusy', 'pussi[^l]', 'pusses'
        ],
    ' nigger ':
        [
            'nigger', 'ni[g]+a', ' nigr ', 'niguh', 'n3gr', 'n i g g e r'
        ],
    ' shut the fuck up ':
        [
            'stfu'
        ],
    ' idiot ':
        [
            'i[d]+io[t]+', '(i)([^a-z ]*)(d)([^a-z ]*)(i)([^a-z ]*)(o)([^a-z ]*)(t)', 'idiots', 'i d i o t'
        ],
    ' dumb ass ':
        [
            'dumbass', 'dubass'
        ],
    ' faggot ':
        [
            'fa[g]+[s]*[^a-z ]', 'fagot', 'f a g g o t', 'faggit',
            '(f)([^a-z ]*)(a)([^a-z ]*)([g]+)([^a-z ]*)(o)([^a-z ]*)(t)', 'fau[g]+ot', 'fae[g]+ot',
        ],
    ' whore ':
        [
            'w h o r e'
        ],
}