#!/usr/bin/python3
import imdb
import sys
import urllib
import random
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLineEdit, QMessageBox, QLabel)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
import operator

idList = []
titleList = []
yearList = []
genreList = []
imdbIdList = []

datafile = open("movies.csv", 'r')
datafile.readline()
for line in datafile:
    if(line.count('"') == 0):
        data = line.split(",")
        idList.append(data[0])
        title = data[1].split("(")
        splitGenres = data[2].split('|')
        # print(splitGenres)
        genreList.append(splitGenres)
        data[3] = data[3].replace("\n", "")
        imdbIdList.append(data[3])
        # print(data)

        if(len(title) == 2):
            titleList.append(title[0])
            title[1] = title[1].replace(")", "")
            yearList.append(title[1])
        if(len(title) == 3):
            # print(title)
            title[0] += "("
            title[0] += title[1]
            # print(title[0])
            titleList.append(title[0])
            title[2] = title[2].replace(")", "")
            yearList.append(title[2])
        if(len(title) == 1):
            titleList.append(title[0])
            yearList.append('0')
        if(len(title) == 4):
            # print(title)
            title[0] += "("
            title[0] += title[1]
            title[0] += "("
            title[0] += title[2]
            # print(title[0])
            titleList.append(title[0])
            title[3] = title[3].replace(")", "")
            yearList.append(title[3])
        if(len(title) == 5):
            title[0] += "("
            title[0] += title[1]
            title[0] += "("
            title[0] += title[2]
            title[0] += "("
            title[0] += title[3]
            # print(title[0])
            titleList.append(title[0])
            title[4] = title[4].replace(")", "")
            yearList.append(title[4])

    if(line.count('"') == 2):
        data = line.split('"')
        idList.append(data[0])
        genreSplit = data[2].split(',')
        # print(genreSplit)
        splitGenres = genreSplit[1].split('|')
        genreList.append(splitGenres)
        genreSplit[2] = genreSplit[2].replace("\n", "")
        imdbIdList.append(genreSplit[2])
        titleToSplit = data[1].split("(")
        if(titleToSplit[1].count('Das Mill') == 1):
            titleToSplit[0] += titleToSplit[1]
            titleList.append(titleToSplit[0])
            yearList.append('0')
            continue
        if(titleToSplit[1].count('Bicicleta') == 1):
            titleToSplit[0] += titleToSplit[1]
            titleList.append(titleToSplit[0])
            yearList.append('0')
            continue
        else:
            titleList.append(titleToSplit[0])

        if(len(titleToSplit) == 2):
            titleToSplit[1] = titleToSplit[1].replace(")", "")
            yearList.append(titleToSplit[1])
        if(len(titleToSplit) == 3):
            # print(titleToSplit)
            titleToSplit[2] = titleToSplit[2].replace(")", "")
            yearList.append(titleToSplit[2])
        if(len(titleToSplit) != 2 and len(titleToSplit) != 3):
            # aSum += 1
            # print(len(titleToSplit))
            # print(titleToSplit)
            yearToFind = len(titleToSplit) - 1
            titleToSplit[yearToFind] = titleToSplit[yearToFind].replace(")", "")
            yearList.append(titleToSplit[yearToFind])

    if(line.count('"') == 4):
        # print(line)
        data = line.split(',')
        # print(data)
        idList.append(data[0])
        splitGenres = data[2].split('|')
        genreList.append(splitGenres)
        data[3] = data[3].replace("\n", "")
        imdbIdList.append(data[3])
        titleToSplit = data[1].split("(")
        titleList.append(titleToSplit[0])
        titleToSplit[1] = titleToSplit[1].replace(")", "")
        yearList.append(titleToSplit[1])

    if(line.count('"') == 6):
        # print(line)
        if(line.count("Cats") == 1):
            # print(line)
            data = line.split(',')
            idList.append(data[0])
            splitGenres = data[2].split('|')
            genreList.append(splitGenres)
            data[3] = data[3].replace("\n", "")
            imdbIdList.append(data[3])
            titleToSplit = data[1].split("(")
            titleList.append(titleToSplit[0])
            titleToSplit[1] = titleToSplit[1].replace(")", "")
            yearList.append(titleToSplit[1])
            # print(data)
        if(line.count("Die") == 1):
            data = line.split(",")
            idList.append(data[0])
            splitGenres = data[2].split('|')
            genreList.append(splitGenres)
            # genreList.append(data[2])
            data[3] = data[3].replace("\n", "")
            imdbIdList.append(data[3])
            titleToSplit = data[1].split("(")
            titleList.append(titleToSplit[0])
            titleToSplit[1] = titleToSplit[1].replace(")", "")
            yearList.append(titleToSplit[1])
            # print(line)

# def titleSearch(stringToSearchFor):
#     for i in range(0, len(titleList)):
#         if(titleList[i].count(stringToSearchFor) > 0):
#             print(titleList[i])

# print()
# print("idlist")
# print(len(idList))
# print("titleList")
# print(len(titleList))
# print("yearList")
# print(len(yearList))
# print("imdbList")
# print(len(imdbIdList))
# print("genreList")
# print(len(genreList))
# print("total Entries: 27278")
# print(genreList)

# design the dataframe

# df['id', 'title', 'year', 'genre', 'imdbid']
df = pd.DataFrame(columns= ['id', 'title', 'year', 'genre', 'imdbid'])
df['id'] = idList
df['title'] = titleList
df['year'] = yearList
df['genre'] = genreList
df['imdbid'] = imdbIdList
# print(df)

userSelectedDf = pd.DataFrame(columns= ['id', 'title', 'year', 'genre', 'imdbid'])

ia = imdb.IMDb()
uiLayout = QVBoxLayout()

randomMovieIndexList = []
chosenMovieIndexList = []

userSelectedList = []

def weighted_jaccard_similarity(listOfGenres,genresComparedToMovie):
    # in this case, 'a' is all the selections that the user has made so far
    # build the weighted dictionary:
    weightedDict = {'total': 0}
    for el in listOfGenres:
        for genre in el:
            #print(genre)
            if genre in weightedDict: weightedDict[genre] += 1
            else: weightedDict[genre] = 1
            weightedDict['total'] += 1

    #print('weighted dictionary:')
    #print(c)

    #print("compared to:")
    #print(b)

    numerator = 0
    denomenator = weightedDict['total']
    for genre in genresComparedToMovie:
        if genre in weightedDict:
            numerator += weightedDict[genre]

    #print('\n\nNumerator = ' + str(numerator))
    #print('Denominator = ' + str(denomenator))

    return numerator / denomenator

# looks at the entire data set ('data')
# and returns the k nearest neighbors based on the distance metric
# 'target' is the movie that we are comparing to
# returns the index of the k movies that are closest
def getNeighbors(data, target, k):
    distances = []
    for x in range(len(data)):
        dist = weighted_jaccard_similarity(target, data[x])
        distances.append((x, data[x], dist))
    distances.sort(key=operator.itemgetter(2), reverse=True)  # sort based on the distance
    # print("\nThe raw distance information sorted:")
    # print(distances)
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def clickable(widget):

    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'CS 3580 Assignment 6 Dylan Waters'
        self.left = 1
        self.top = 1
        self.width = 1500
        self.height = 150
        self.hasSearched = 0
        self.initUI()

    def initUI(self):
        movieNames = QHBoxLayout()
        movieRatings = QHBoxLayout()
        movieImages = QHBoxLayout()
        searchLayout = QHBoxLayout()

        self.movieNames = movieNames
        self.movieRatings = movieRatings
        self.movieImages = movieImages
        # display 10 movies at random
        for i in range(0, 9):
            print("generating movie " + str(i))
            # get a random movie
            newMovieListValue = random.randint(0,len(titleList) - 1)
            randomMovieIndexList.append(newMovieListValue)
            movie = ia.get_movie(imdbIdList[newMovieListValue])
            # acquire images and rating to display
            imgUrl = movie['cover url']
            movieUrl = urllib.request.urlopen(imgUrl).read()
            rating = movie['rating']
            movieNameLabel = QLabel(titleList[newMovieListValue])
            movieLabel = QLabel(self)
            movieImg = QPixmap()
            movieRating = QLabel(str(rating) + "/10")

            movieImg.loadFromData(movieUrl)
            movieLabel.setPixmap(movieImg)
            # movieLabel.clicked.connect(self(newMovieListValue))
            clickable(movieLabel).connect(partial(self.findNewMovies, newMovieListValue))
            # movieLabel.mousePressEvent = self.findNewMovies(newMovieListValue)
            # movieLabel.clicked.connect(self.findNewMovies(newMovieListValue))
            movieNames.addWidget(movieNameLabel)
            movieImages.addWidget(movieLabel)
            movieRatings.addWidget(movieRating)

        # create the ui
        self.searchBox = QLineEdit(self)
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(self.movieSearch)
        self.searchBox.resize(900, 20)
        searchButton.resize(50, 20)
        searchLayout.addWidget(self.searchBox)
        searchLayout.addWidget(searchButton)

        uiLayout.addLayout(movieNames)
        uiLayout.addLayout(movieImages)
        uiLayout.addLayout(movieRatings)
        uiLayout.addLayout(searchLayout)
        self.setLayout(uiLayout)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def movieSearch(self):
        textValue = self.searchBox.text()
        totalMoviesFound = 0
        movieNamesSearch = QHBoxLayout()
        movieRatingsSearch = QHBoxLayout()
        movieImagesSearch = QHBoxLayout()
        if(self.hasSearched):
            # print("attempting to remove layout items")
            print(self.movieRatingsSearch.count())
            for i in reversed(range(self.movieRatingsSearch.count())):
                # print(i)
                # if isinstance(i, QWidgetItem):
                self.movieNamesSearch.itemAt(i).widget().setParent(None)
                self.movieImagesSearch.itemAt(i).widget().setParent(None)
                self.movieRatingsSearch.itemAt(i).widget().setParent(None)

                # uiLayout.itemAt(i).widget().deleteLater()
            # uiLayout.removeItem(movieNamesSearch)
            # # uiLayout.movieNamesSearch.setParent(None)
            # uiLayout.removeItem(movieImagesSearch)
            # uiLayout.removeItem(movieRatingsSearch)
            # uiLayout.deleteLater(movieNamesSearch)
            # uiLayout.itemAt(5).setParent(None)
            # uiLayout.itemAt(6).setParent(None)
            # uiLayout.itemAt(7).setParent(None)

        # self.sender().obj.index

        self.movieNamesSearch = movieNamesSearch
        self.movieImagesSearch = movieImagesSearch
        self.movieRatingsSearch = movieRatingsSearch
        self.hasSearched = 1
        for i in range(0, len(titleList)):
            if(totalMoviesFound > 9):
                break
            if(titleList[i].count(textValue) > 0):
                totalMoviesFound += 1
                print(titleList[i])

                movie = ia.get_movie(imdbIdList[i])
                # acquire images and rating to display
                imgUrl = movie['cover url']
                movieUrl = urllib.request.urlopen(imgUrl).read()
                rating = movie['rating']
                movieLabel = QLabel(self)
                movieImg = QPixmap()
                movieRating = QLabel(str(rating) + "/10")
                movieNameLabel = QLabel(titleList[i])

                movieImg.loadFromData(movieUrl)
                movieLabel.setPixmap(movieImg)
                clickable(movieLabel).connect(partial(self.findNewMovies, i))
                # movieLabel.mouseReleaseEvent = self.findNewMovies(i)
                movieNamesSearch.addWidget(movieNameLabel)
                movieImagesSearch.addWidget(movieLabel)
                movieRatingsSearch.addWidget(movieRating)
            if(yearList[i].count(textValue) > 0):
                totalMoviesFound += 1
                print(titleList[i])

                movie = ia.get_movie(imdbIdList[i])
                # acquire images and rating to display
                imgUrl = movie['cover url']
                movieUrl = urllib.request.urlopen(imgUrl).read()
                rating = movie['rating']
                movieLabel = QLabel(self)
                movieImg = QPixmap()
                movieRating = QLabel(str(rating) + "/10")
                movieNameLabel = QLabel(titleList[i])

                movieImg.loadFromData(movieUrl)
                movieLabel.setPixmap(movieImg)
                clickable(movieLabel).connect(partial(self.findNewMovies, i))
                # movieLabel.mouseReleaseEvent = self.findNewMovies()
                movieNamesSearch.addWidget(movieNameLabel)
                movieImagesSearch.addWidget(movieLabel)
                movieRatingsSearch.addWidget(movieRating)
            if(genreList[i].count(textValue) > 0):
                totalMoviesFound += 1
                print(titleList[i])

                movie = ia.get_movie(imdbIdList[i])
                # acquire images and rating to display
                imgUrl = movie['cover url']
                movieUrl = urllib.request.urlopen(imgUrl).read()
                rating = movie['rating']
                movieLabel = QLabel(self)
                movieImg = QPixmap()
                movieRating = QLabel(str(rating) + "/10")
                movieNameLabel = QLabel(titleList[i])

                movieImg.loadFromData(movieUrl)
                movieLabel.setPixmap(movieImg)
                clickable(movieLabel).connect(partial(self.findNewMovies, i))
                # movieLabel.mouseReleaseEvent = self.findNewMovies
                movieNamesSearch.addWidget(movieNameLabel)
                movieImagesSearch.addWidget(movieLabel)
                movieRatingsSearch.addWidget(movieRating)
        self.movieNamesSearch = movieNamesSearch
        self.movieImagesSearch = movieImagesSearch
        self.movieRatingsSearch = movieRatingsSearch
        uiLayout.addLayout(movieNamesSearch)
        # print(uiLayout.count())
        uiLayout.addLayout(movieImagesSearch)
        # print(uiLayout.count())
        uiLayout.addLayout(movieRatingsSearch)
        # print(uiLayout.count())
        # print(self.entries)
        # for i in reversed(range(uiLayout.count())):
        #     print(i)

    def findNewMovies(self, newMovieListValue):
        # selectedIndex = self.sender()
        userSelectedList.append(genreList[newMovieListValue])
        userSelectedDf.loc[df.index[newMovieListValue]] = df.iloc[newMovieListValue]
        print(userSelectedDf)
        for i in reversed(range(self.movieNames.count())):
            self.movieNames.itemAt(i).widget().setParent(None)
            self.movieImages.itemAt(i).widget().setParent(None)
            self.movieRatings.itemAt(i).widget().setParent(None)
        neighborResult = getNeighbors(genreList, userSelectedList, k=10)
        print(neighborResult)

        for i in range(0, 9):
            print("generating movie " + str(i))
            # get a random movie
            newMovieListValue = neighborResult[i]
            randomMovieIndexList.append(newMovieListValue)
            movie = ia.get_movie(imdbIdList[newMovieListValue])
            # acquire images and rating to display
            imgUrl = movie['cover url']
            movieUrl = urllib.request.urlopen(imgUrl).read()
            rating = movie['rating']
            movieNameLabel = QLabel(titleList[newMovieListValue])
            movieLabel = QLabel(self)
            movieImg = QPixmap()
            movieRating = QLabel(str(rating) + "/10")

            movieImg.loadFromData(movieUrl)
            movieLabel.setPixmap(movieImg)
            # movieLabel.clicked.connect(self(newMovieListValue))
            clickable(movieLabel).connect(partial(self.findNewMovies, newMovieListValue))
            # movieLabel.mousePressEvent = self.findNewMovies(newMovieListValue)
            # movieLabel.clicked.connect(self.findNewMovies(newMovieListValue))
            self.movieNames.addWidget(movieNameLabel)
            self.movieImages.addWidget(movieLabel)
            self.movieRatings.addWidget(movieRating)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
