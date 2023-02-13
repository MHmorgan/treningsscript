module Page.Start exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, href)
import Skeleton

{-| Start handles the start page where you can
start training sessions from.

-}


-- VIEW


view : Skeleton.Details never
view =
  { title = "Training App"
  , header = "Start Training 🏋️"
  , attrs = []
  , kids =
    [ a [ class "btn btn-outline-success", href "/start" ] [ text "Start" ]
    , a [ class "btn btn-outline-success", href "/session?day=Pull" ] [ text "Pull" ]
    , a [ class "btn btn-outline-success", href "/session?day=Push" ] [ text "Push" ]
    , a [ class "btn btn-outline-success", href "/session?day=Legs" ] [ text "Legs" ]
    , a [ class "btn btn-outline-success", href "/session?day=Core" ] [ text "Core" ]
    , a [ class "btn btn-outline-success", href "/session?day=Cardio" ] [ text "Cardio" ]
    ]
  }
