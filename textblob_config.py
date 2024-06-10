class Word(str):

    """A simple word representation. Includes methods for inflection,
    translation, and WordNet integration.
    """

    def __new__(cls, string, pos_tag=None):
        """Return a new instance of the class. It is necessary to override
        this method in order to handle the extra pos_tag argument in the
        constructor.
        """
        return super().__new__(cls, string)

    def __init__(self, string, pos_tag=None):
        self.string = string
        self.pos_tag = pos_tag

    def __repr__(self):
        return repr(self.string)

    def __str__(self):
        return self.string

    def singularize(self):
        """Return the singular version of the word as a string."""
        return Word(_singularize(self.string))

    def pluralize(self):
        """Return the plural version of the word as a string."""
        return Word(_pluralize(self.string))

    def spellcheck(self):
        """Return a list of (word, confidence) tuples of spelling corrections.

        Based on: Peter Norvig, "How to Write a Spelling Corrector"
        (http://norvig.com/spell-correct.html) as implemented in the pattern
        library.

        .. versionadded:: 0.6.0
        """
        return suggest(self.string)

    def correct(self):
        """Correct the spelling of the word. Returns the word with the highest
        confidence using the spelling corrector.

        .. versionadded:: 0.6.0
        """
        return Word(self.spellcheck()[0][0])

    @cached_property
    @requires_nltk_corpus
    def lemma(self):
        """Return the lemma of this word using Wordnet's morphy function."""
        return self.lemmatize(pos=self.pos_tag)

    @requires_nltk_corpus
    def lemmatize(self, pos=None):
        """Return the lemma for a word using WordNet's morphy function.

        :param pos: Part of speech to filter upon. If `None`, defaults to
            ``_wordnet.NOUN``.

        .. versionadded:: 0.8.1
        """
        if pos is None:
            tag = _wordnet.NOUN
        elif pos in _wordnet._FILEMAP.keys():
            tag = pos
        else:
            tag = _penn_to_wordnet(pos)
        lemmatizer = nltk.stem.WordNetLemmatizer()
        return lemmatizer.lemmatize(self.string, tag)

    PorterStemmer = nltk.stem.porter.PorterStemmer()
    LancasterStemmer = nltk.stem.lancaster.LancasterStemmer()
    SnowballStemmer = nltk.stem.snowball.SnowballStemmer("english")

    # added 'stemmer' on lines of lemmatizer
    # based on nltk
    def stem(self, stemmer=PorterStemmer):
        """Stem a word using various NLTK stemmers. (Default: Porter Stemmer)

        .. versionadded:: 0.12.0
        """
        return stemmer.stem(self.string)

    @cached_property
    def synsets(self):
        """The list of Synset objects for this Word.

        :rtype: list of Synsets

        .. versionadded:: 0.7.0
        """
        return self.get_synsets(pos=None)

    @cached_property
    def definitions(self):
        """The list of definitions for this word. Each definition corresponds
        to a synset.

        .. versionadded:: 0.7.0
        """
        return self.define(pos=None)

    def get_synsets(self, pos=None):
        """Return a list of Synset objects for this word.

        :param pos: A part-of-speech tag to filter upon. If ``None``, all
            synsets for all parts of speech will be loaded.

        :rtype: list of Synsets

        .. versionadded:: 0.7.0
        """
        return _wordnet.synsets(self.string, pos)

    def define(self, pos=None):
        """Return a list of definitions for this word. Each definition
        corresponds to a synset for this word.

        :param pos: A part-of-speech tag to filter upon. If ``None``, definitions
            for all parts of speech will be loaded.
        :rtype: List of strings

        .. versionadded:: 0.7.0
        """
        return [syn.definition() for syn in self.get_synsets(pos=pos)]