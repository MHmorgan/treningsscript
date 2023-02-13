module Page.Session.Exercise exposing (..)

import Html exposing (..)
import Page.Session as Session


-- MODEL


type alias Model =
    { exercise : Session.Exercise
    }


init : Session.Exercise -> Model
init exercise =
    { exercise = exercise
    }



-- VIEW


view : Model -> Html Session.Msg
view model =
    div [] [ text "Exercise" ]
