import unittest
from unittest.mock import Mock, patch
from quartz.log import Log
from ds.sqlite._data import *

unittest.TestLoader.sortTestMethodsUsing = None


class TestBase:

    def setUp(self):
        # Publishers
        self.small = self.small_ = None
        self.modest = self.modest_ = None
        self.big = self.big_ = None
        # Genres
        self.adventure = Genre("Adventure")
        self.comedy = Genre("Funny")
        self.fantasy = Genre("Fantasy")
        self.novel = Genre("Novel")
        self.satire = Genre("Satire")
        self.sci_fi = Genre("Sci-fi")
        self.adventure_ = None
        self.comedy_ = None
        self.fantasy_ = None
        self.novel_ = None
        self.satire_ = None
        self.sci_fi_ = None
        # Authors
        self.adams = Author("Douglas Adams")
        self.asturias = Author("Miguel Ángel Asturias")
        self.brown = Author("Dan Brown")
        self.dumas = Author("Alexandre Dumas")
        self.cervantes = Author("Miguel de Cervantes Saavedra")
        self.gabo = Author("Gabo")
        self.hebert = Author("Frank Herbert")
        self.homer = Author("Homer")
        self.orwell = Author("George Orwell")
        self.swift = Author("Jonathan Swift")
        self.adams_ = None
        self.asturias_ = None
        self.brown_ = None
        self.dumas_ = None
        self.cervantes_ = None
        self.gabo_ = None
        self.hebert_ = None
        self.homer_ = None
        self.orwell_ = None
        self.swift_ = None
        # Books
        self.illiad = self.illiad_ = None
        self.odyssey = self.odyssey_ = None
        self.quixote = self.quixote_ = None
        self.gulliver = self.gulliver_ = None
        self.le_comte = self.le_comte_ = None
        self.les_trois = self.les_trois_ = None
        self.animal = self.animal_ = None
        self.ninety = self.ninety_ = None
        self.maize = self.maize_ = None
        self.dune = self.dune_ = None
        self.solitude = self.solitude_ = None
        self.hitchhiker = self.hitchhiker_ = None
        self.restaurant = self.restaurant_ = None
        self.everything = self.everything_ = None
        self.thanks = self.thanks_ = None
        self.harmless = self.harmless_ = None
        self.the_code = self.the_code_ = None
        self.fakebook = self.fakebook_ = None
        self.books = self.books_ = []

    def tearDown(self):
        pass


class TestA(TestBase, unittest.TestCase):

    def testDataset(self):
        Log.test("\nTest Dataset")
        ds = Dataset("examples/db/books.sql")
        ds.open("temp/books.db", reset=True)
        self.checkAdd(ds)
        self.checkAddJoins(ds)
        self.checkUpdate(ds)
        self.checkReadRefs(ds)
        self.checkReadData(ds)
        self.checkReadJoins(ds)
        self.checkDeleteJoins(ds)
        self.checkDeleteEntities(ds)
        ds.print()

    def checkAdd(self, ds):
        Log.list("Create")
        # Publishers
        self.big = Publisher(None, "Big Editorial")
        self.big_ = ds.publishers.add(self.big)
        self.small = Publisher(self.big_, "Small Books")
        self.small_ = ds.publishers.add(self.small)
        self.modest = Publisher(self.big_, "Modest Reads")
        self.modest_ = ds.publishers.add(self.modest)
        # Genres
        self.adventure_ = ds.genres.add(self.adventure)
        self.comedy_ = ds.genres.add(self.comedy)
        self.fantasy_ = ds.genres.add(self.fantasy)
        self.novel_ = ds.genres.add(self.novel)
        self.satire_ = ds.genres.add(self.satire)
        self.sci_fi_ = ds.genres.add(self.sci_fi)
        self.genres = [
            self.adventure,
            self.comedy,
            self.fantasy,
            self.novel,
            self.satire,
            self.sci_fi,
        ]
        for g in self.genres:
            self.assertIsNotNone(g)
            self.assertIsNotNone(g.id)
        # Authors
        self.adams_ = ds.authors.add(self.adams)
        self.asturias_ = ds.authors.add(self.asturias)
        self.brown_ = ds.authors.add(self.brown)
        self.cervantes_ = ds.authors.add(self.cervantes)
        self.dumas_ = ds.authors.add(self.dumas)
        self.gabo_ = ds.authors.add(self.gabo)
        self.hebert_ = ds.authors.add(self.hebert)
        self.homer_ = ds.authors.add(self.homer)
        self.orwell_ = ds.authors.add(self.orwell)
        self.swift_ = ds.authors.add(self.swift)
        self.authors = [
            self.adams,
            self.asturias,
            self.brown,
            self.cervantes,
            self.dumas,
            self.gabo,
            self.hebert,
            self.homer,
            self.orwell,
            self.swift,
        ]
        for a in self.authors:
            self.assertIsNotNone(a)
            self.assertIsNotNone(a.id)
        # Books
        self.illiad = Book(self.small, "The Iliad", 700)
        self.odyssey = Book(self.small, "The Odyssey", 701)  # Intentional: wrong author
        self.quixote = Book(self.modest, "Don Quixote", 1605)
        self.gulliver = Book(self.modest, "Gulliver's Travels", 1726)
        self.le_comte = Book(self.modest, "Le Comte de Monte-Cristo", 1944)  # Intentional: wrong author, year
        self.les_trois = Book(self.modest, "Les Trois Mousquetaires", 1894)
        self.animal = Book(self.big, "Animal Farm", 1945)
        self.ninety = Book(self.big, "1984", 1949)
        self.maize = Book(self.big, "Hombres de maíz", 1949)
        self.dune = Book(self.big, "Dune", 1965)
        self.solitude = Book(self.big, "Cien años de soledad", 1967)
        self.hitchhiker = Book(self.big, "The Hitchhiker's Guide to the Galaxy", 1979)
        self.restaurant = Book(
            self.big, "The Restaurant at the End of the Universe", 1980
        )
        self.everything = Book(self.big, "Life, the Universe and Everything", 1982)
        self.thanks = Book(self.big, "So Long, and Thanks for All the Fish", 1984)
        self.harmless = Book(self.big, "Mostly Harmless", 1892)  # Intentional: wrong author, year
        self.the_code = Book(self.big, "The Da Vinci Code", 2003)  # Intentional: wrong author
        self.fakebook = Book(self.big, "Fakebook", 2005)  # Intentional: wrong author
        self.books = [
            self.illiad,
            self.odyssey,
            self.quixote,
            self.gulliver,
            self.le_comte,
            self.les_trois,
            self.animal,
            self.ninety,
            self.maize,
            self.dune,
            self.solitude,
            self.hitchhiker,
            self.restaurant,
            self.everything,
            self.thanks,
            self.harmless,
            self.the_code,
            self.fakebook,
        ]
        self.illiad_ = ds.books.add(self.illiad)
        self.odyssey_ = ds.books.add(self.odyssey)
        self.quixote_ = ds.books.add(self.quixote)
        self.gulliver_ = ds.books.add(self.gulliver)
        self.le_comte_ = ds.books.add(self.le_comte)
        self.les_trois_ = ds.books.add(self.les_trois)
        self.animal_ = ds.books.add(self.animal)
        self.ninety_ = ds.books.add(self.ninety)
        self.maize_ = ds.books.add(self.maize)
        self.dune_ = ds.books.add(self.dune)
        self.solitude_ = ds.books.add(self.solitude)
        self.hitchhiker_ = ds.books.add(self.hitchhiker)
        self.restaurant_ = ds.books.add(self.restaurant)
        self.everything_ = ds.books.add(self.everything)
        self.thanks_ = ds.books.add(self.thanks)
        self.harmless_ = ds.books.add(self.harmless)
        self.the_code_ = ds.books.add(self.the_code)
        self.fakebook_ = ds.books.add(self.fakebook)
        self.books_ = [
            self.illiad_,
            None,
            self.quixote_,
            self.gulliver_,
            self.le_comte_,
            self.les_trois_,
            self.animal_,
            self.ninety_,
            self.maize_,
            self.dune_,
            self.solitude_,
            self.hitchhiker_,
            self.restaurant_,
            self.everything_,
            self.thanks_,
            self.harmless_,
            self.the_code_,
            None,
        ]
        for b in self.books_:
            if b:
                self.assertIsNotNone(b.id)

    def checkAddJoins(self, ds):
        Log.list("Add Joins")
        # author -> book
        ds.books.link(self.fakebook_, self.dumas_)  # Intentionally wrong
        # book -> author
        ds.books.link(self.illiad_, self.homer_)
        ds.books.link(self.odyssey_, self.homer_)
        ds.books.link(self.quixote_, self.cervantes_)
        ds.books.link(self.gulliver_, self.swift_)
        ds.books.link(self.les_trois_, self.dumas_)
        ds.books.link(self.animal_, self.orwell_)
        ds.books.link(self.ninety_, self.orwell_)
        ds.books.link(self.maize_, self.asturias_)
        ds.books.link(self.dune_, self.hebert_)
        ds.books.link(self.solitude_, self.gabo_)
        ds.books.link(self.hitchhiker_, self.adams_)
        ds.books.link(self.restaurant_, self.adams_)
        ds.books.link(self.everything_, self.adams_)
        ds.books.link(self.thanks_, self.adams_)
        ds.books.link(self.harmless_, self.adams_)
        ds.books.link(self.the_code_, self.brown_)
        ds.books.link(self.fakebook_, self.cervantes_)  # Intentionally wrong
        # book -> genre
        ds.books.link(self.illiad, ds.genres.ref("Adventure"))
        ds.books.link(self.quixote, self.novel)
        ds.books.link(self.gulliver, self.satire)
        ds.books.link(self.le_comte, self.adventure)
        ds.books.link(self.les_trois, ds.genres.ref("Novel"))
        ds.books.link(self.animal, self.satire)
        ds.books.link(self.ninety, self.fantasy)
        ds.books.link(self.ninety, ds.genres.ref("Satire"))
        ds.books.link(self.dune, self.sci_fi)
        ds.books.link(self.maize, self.novel)
        ds.books.link(self.dune, self.sci_fi)
        ds.books.link(self.dune, self.comedy)  # To be deleted
        ds.books.link(self.dune, self.satire)  # To be deleted
        # genre -> book
        ds.books.link(self.animal, self.adventure)  # To be deleted
        ds.books.link(self.ninety, self.comedy)  # To be deleted
        ds.books.link(ds.books.ref("Dune"), self.sci_fi)
        ds.books.link(self.solitude, self.fantasy)
        ds.books.link(self.hitchhiker, self.comedy)
        ds.books.link(self.restaurant, self.comedy)
        ds.books.link(self.everything, self.comedy)
        ds.books.link(self.thanks, self.comedy)
        ds.books.link(self.harmless, self.comedy)
        ds.books.link(self.hitchhiker, self.sci_fi)
        ds.books.link(self.restaurant, self.sci_fi)
        ds.books.link(self.everything, self.sci_fi)
        ds.books.link(self.thanks, self.sci_fi)
        ds.books.link(self.harmless, self.sci_fi)

    def checkUpdate(self, ds):
        Log.list("Update")
        # Update author
        name = "Gabiel García Márquez"
        self.gabo.name = name
        ds.authors.update(self.gabo)
        a = ds.authors.one(self.gabo)
        self.assertEqual(a.name, name)
        # Update genre
        name = "Comedy"
        self.comedy.name = name
        ds.genres.update(self.comedy)
        g = ds.genres.one(self.comedy)
        self.assertEqual(g.name, name)
        # Update book
        title = "The Count of Monte-Cristo"
        year = 1844
        self.le_comte.title = title
        self.le_comte.year = year
        ds.books.update(self.le_comte)
        ds.books.link(self.le_comte, self.dumas)
        b = ds.books.one(self.le_comte)
        self.assertEqual(b.title, title)
        self.assertEqual(b.year, year)
        authors = ds.authors.refs(self.le_comte)
        self.assertTrue(self.dumas in authors)
        # Update book
        title = self.harmless.title
        year = 1992
        ds.books.link(self.harmless, self.adams)
        self.harmless.year = year
        self.harmless = ds.books.update(self.harmless)
        b = ds.books.one(self.harmless)
        self.assertEqual(b.title, title)
        self.assertEqual(b.year, year)
        authors = ds.authors.refs(self.harmless)
        self.assertTrue(self.adams in authors)

    def checkReadRefs(self, ds):
        Log.list("Read Refs")
        # Genres
        genres = ds.genres.refs()
        self.assertEqual(len(genres), len(self.genres))
        for i in range(0, len(genres)):
            self.assertEqual(genres[i], self.genres[i])
        # Authors
        authors = ds.authors.refs()
        self.assertEqual(len(authors), len(self.authors))
        for i in range(0, len(authors)):
            if authors[i] != self.authors[i]:
                n = [r.id() for r in self.authors]
                m = [r.id() for r in authors]
                Log.debug("N: {}".format(n))
                Log.debug("M: {}".format(m))
                Log.debug("?")
            self.assertEqual(authors[i].id, self.authors[i].id)
        # Books
        books = ds.books.refs()
        self.assertEqual(len(books), len(self.books))
        for b in books:
            self.assertTrue(b in self.books)
        # By year
        expected = [self.ninety, self.maize]
        books = ds.books.refs(YearFilter(1949))
        self.assertEqual(len(books), len(expected))
        for b in books:
            self.assertTrue(b in expected)

    def checkReadData(self, ds):
        Log.list("Read Data")
        # Genres
        genres = ds.genres.all()
        self.assertEqual(len(genres), len(self.genres))
        for i in range(0, len(genres)):
            self.assertEqual(genres[i].name, self.genres[i].name)
        # Authors
        authors = ds.authors.all()
        self.assertEqual(len(authors), len(self.authors))
        for i in range(0, len(authors)):
            self.assertEqual(authors[i].name, self.authors[i].name)
        # Books
        books = ds.books.all()
        self.assertEqual(len(books), len(self.books))
        books_ = [b.title for b in self.books]
        for i in range(0, len(books)):
            # self.assertEqual(books[i].name, self.books[i].name)
            self.assertTrue(books[i].title in books_)

    def checkReadJoins(self, ds):
        Log.list("Read Joins")
        # Book -> Genres (refs)
        expected = [self.comedy, self.satire, self.sci_fi]
        genres = ds.genres.refs(self.dune)
        self.assertEqual(len(genres), len(expected))
        for g in genres:
            self.assertTrue(g in expected)
        # Book -> Genres (data)
        expected = [self.comedy.name, self.satire.name, self.sci_fi.name]
        genres = ds.genres.all(self.dune)
        self.assertEqual(len(genres), len(expected))
        for g in genres:
            self.assertTrue(g.name in expected)
        # Genre --> Books
        expected = [
            self.dune,
            self.hitchhiker,
            self.restaurant,
            self.everything,
            self.thanks,
            self.harmless,
        ]
        books = ds.books.refs(self.sci_fi)
        self.assertEqual(len(books), len(expected))
        # Genre --> Books (data)
        expected = [
            self.dune.title,
            self.hitchhiker.title,
            self.restaurant.title,
            self.everything.title,
            self.thanks.title,
            self.harmless.title,
        ]
        books = ds.books.all(self.sci_fi)
        self.assertEqual(len(books), len(expected))
        for b in books:
            self.assertTrue(b.title in expected)

    def checkDeleteJoins(self, ds):
        Log.list("Delete Joins")
        # Delete author
        ds.books.unlink(self.fakebook_, self.cervantes)
        # Delete book
        ds.books.unlink(self.fakebook, self.dumas)
        # Delete book genre
        ds.books.unlink(self.dune, self.comedy)
        ds.books.unlink(self.dune, self.fantasy)
        ds.books.unlink(self.dune, self.satire)
        # Delete genre book
        ds.books.unlink(self.animal, self.adventure)
        ds.books.unlink(self.dune, self.comedy)
        ds.books.unlink(self.ninety, self.comedy)
        # Check book genres (refs)
        expected = [
            self.hitchhiker,
            self.restaurant,
            self.everything,
            self.thanks,
            self.harmless,
        ]
        books = ds.books.all(ds.genres.ref("Comedy"))
        self.assertEqual(len(books), len(expected))
        for b in books:
            self.assertTrue(b in expected)
        # Check book genre (refs)
        expected = [self.sci_fi]
        genres = ds.genres.refs(self.dune)
        self.assertEqual(len(genres), len(expected))
        for g in genres:
            self.assertTrue(g in expected)
        # Check book genres (data)
        expected = [self.sci_fi.name]
        genres = ds.genres.all(self.dune)
        self.assertEqual(len(genres), len(expected))
        for g in genres:
            self.assertTrue(g.name in expected)
        # Check author books (refs)
        expected = [self.les_trois, self.le_comte]
        books = ds.books.refs(self.dumas)
        self.assertEqual(len(books), len(expected))
        for b in books:
            self.assertTrue(b in expected)
        # Check author books (data)
        expected = [self.quixote.title]
        books = ds.books.all(self.cervantes)
        self.assertEqual(len(books), len(expected))
        for b in books:
            self.assertTrue(b.title in expected)

    def checkDeleteEntities(self, ds):
        Log.list("Delete Entities")
        # Genres
        self.assertIsNotNone(ds.genres.ref(self.satire))
        ds.genres.remove("Satire")
        self.assertIsNone(ds.genres.ref(self.satire))
        for g in ds.genres.all():
            self.assertTrue(g.name != self.satire.name)
        # Authors
        self.assertIsNotNone(ds.authors.ref(self.brown.name))
        ds.authors.remove(self.brown)
        self.assertIsNone(ds.authors.ref(self.brown.name))
        for a in ds.authors.all():
            self.assertTrue(a.name != self.brown.name)
        # Books
        self.assertIsNotNone(ds.books.one(self.illiad))
        ds.books.remove(self.illiad)
        self.assertIsNone(ds.books.one(self.illiad))
        for b in ds.books.all():
            self.assertTrue(b.title != self.illiad.title)


if __name__ == "__main__":
    unittest.main()
