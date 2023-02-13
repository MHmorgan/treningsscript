module Skeleton exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (class, href, property, rel)
import Json.Encode as Encode


-- DETAILS


type alias Details msg =
  { title: String
  , header: String
  , attrs: List (Attribute msg)
  , kids: List (Html msg)
  }



-- VIEW


view : (a -> msg) -> Details a -> Browser.Document msg
view toMsg details =
  { title =
      details.title
  , body =
      [ metaViewport
      , linkBootstrapCss
      , viewHeader details.header
      , Html.map toMsg <|
          div (class "container" :: details.attrs) details.kids
      ]
  }



-- VIEW META


metaViewport : Html msg
metaViewport =
  node "meta"
    [ property "name" (Encode.string "viewport")
    , property "content" (Encode.string "width=device-width, initial-scale=1")
    ]
    []


linkBootstrapCss : Html msg
linkBootstrapCss =
  node "link"
    [ rel  "stylesheet"
    , href "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
    ]
    []



-- VIEW HEADER


viewHeader : String -> Html msg
viewHeader txt =
  header [ class "container-fluid py-3" ]
    [ div [ class "container" ]
      [ h1
        [ class "display-1" ]
        [ text txt ]
      ]
    ]
