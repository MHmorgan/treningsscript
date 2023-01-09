module Main exposing (main)

import Browser
import Common
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)


-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type Model
  = StartPage
  | ExercisePage


init : Model
init =
  StartPage



-- UPDATE


type Msg
  = ToStartPage
  | ToOvelsePage
  | ToOppvarmingPage
  | ToNyPage


update : Msg -> Model -> Model
update msg model =
  case msg of
    ToStartPage ->
      StartPage
    ToOvelsePage ->
      ExercisePage
    _ ->
      model



-- VIEW


view : Model -> Html Msg
view model =
  case model of
    StartPage ->
      viewStartPage
    ExercisePage ->
      viewExercisePage



-- START PAGE


viewStartPage : Html Msg
viewStartPage =
  Common.page "Trening"
    [ div [ class "container" ]
      (List.map startPageButton
        [ ("Øvelse", ToOvelsePage)
        , ("Oppvarming", ToOppvarmingPage)
        , ("Ny", ToNyPage)
        ])
    ]


startPageButton : (String, Msg) -> Html Msg
startPageButton (label, handler) =
  button
    [ class " container-fluid btn btn-outline-success fs-1 p-3 mt-3"
    , onClick handler
    ]
    [ text label ]


-- EXERCISE PAGE

viewExercisePage : Html Msg
viewExercisePage =
  Common.page "Exercise" []
