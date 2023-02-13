module Main exposing (main)

import Browser
import Browser.Navigation as Nav
import Debug
import Page.Session as Session
import Page.Start as Start
import Skeleton
import Url
import Url.Parser as Parser exposing (Parser, (</>), (<?>), custom, fragment, map, oneOf, s, top)
import Url.Parser.Query as Query



-- MAIN


main : Program () Model Msg
main =
  Browser.application
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    , onUrlChange = UrlChanged
    , onUrlRequest = LinkClicked
    }



-- MODEL


type alias Model =
  { key : Nav.Key
  , page : Page
  }


type Page
  = Start
  | Session Session.Model


init : () -> Url.Url -> Nav.Key -> ( Model, Cmd Msg )
init flags url key =
  let
    model = { key = key, page = Start }
  in
    stepUrl url model



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
  case model.page of
    Session sModel ->
      Sub.map SessionMsg (Session.subscriptions sModel)

    _ ->
      Sub.none



-- UPDATE


type Msg
  = LinkClicked Browser.UrlRequest
  | UrlChanged Url.Url
  | SessionMsg Session.Msg


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    LinkClicked urlRequest ->
      case urlRequest of
        Browser.Internal url ->
          ( model, Nav.pushUrl model.key (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )

    UrlChanged url ->
      stepUrl url model

    SessionMsg sMsg ->
      case model.page of
        Session sessionModel ->
          let
            ( newSessionModel, sessionCmd ) =
              Session.update sMsg sessionModel
          in
            ( { model | page = Session newSessionModel }, Cmd.map SessionMsg sessionCmd )

        _ ->
          ( model, Cmd.none )



-- VIEW


view : Model -> Browser.Document Msg
view model =
  case model.page of
    Start ->
      Skeleton.view never Start.view

    Session sModel ->
      Skeleton.view SessionMsg (Session.view sModel)



-- ROUTER


type Route
  = ToHome
  | ToSession String


stepUrl : Url.Url -> Model -> ( Model, Cmd Msg )
stepUrl url model =
  let
    parser =
      oneOf
        [ route top ToHome
        , route (s "session" <?> Query.string "day")
          (\day -> case day of
            Just s -> ToSession s
            _ -> ToHome
          )
        ]

  in
    case Parser.parse parser url of
      Just ToHome ->
        ( { model | page = Start }
        , Cmd.none
        )

      Just (ToSession day) ->
        let
          ( sModel, sCmd ) = Session.init day
        in
        ( { model | page = Session sModel }
        , Cmd.map SessionMsg sCmd
        )

      Nothing ->
        Debug.todo ("404 Not Found " ++ Url.toString url)


route : Parser a b -> a -> Parser (b -> c) c
route parser handler =
  Parser.map handler parser
