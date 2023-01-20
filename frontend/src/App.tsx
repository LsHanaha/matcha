
import { useEffect, useState, React } from "react";
import {
  BrowserRouter,
  Switch,
  Route,
  Redirect,
  Link
} from "react-router-dom";

const a= 1
function foo (name  ) {
  const last_name="doe"
  const x=200

}
console.log(a  )
function App() {
  const [isUserLoggedIn, setUserLoggedIn] = useState(false);

  useEffect(() => {
    // TODO - add jwt checker is token still valid
  }, []);

  return (
    <div className="App">
        <BrowserRouter>
          <Switch>
            {/* <PrivateRoute
              path={ROUTER_ENDPOINTS.home}
              component={HomePage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              exact
              path={ROUTER_ENDPOINTS.greetings}
              component={GreetingsPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.signIn}
              component={SignInPage}
              isAuthorized={isUserLoggedIn}
              setUserLogged={setUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.signUp}
              component={SignUpPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.emailVerification}
              component={VerifyEmailPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.restoreMail}
              component={RestorePwdMailPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.restorePwd}
              component={RestorePwdPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.newPassword}
              component={NewPasswordPage}
              isAuthorized={isUserLoggedIn}
            /> */}
          </Switch>
        </BrowserRouter>
    </div>
  );
}

// const PrivateRoute = ({
//   component: Component,
//   isAuthorized: isAuthorized,
//   ...rest
// }) => (
//   <Route
//     {...rest}
//     render={(props) => {
//       // eslint-disable-next-line no-unused-expressions
//       return isAuthorized ? <Component {...props} /> : <Redirect to="/" />;
//     }}
//   />
// );

// const UnregisteredRoute = ({
//   component: Component,
//   isAuthorized: isAuthorized,
//   ...rest
// }) => (
//   <Route
//     {...rest}
//     render={(props) => {
//       // eslint-disable-next-line no-unused-expressions
//       return !isAuthorized ? (
//         <Component {...props} {...rest} />
//       ) : (
//         <Redirect to="/home" />
//       );
//     }}
//   />
// );
const foo1 = () => {
  return 1;
}
const bwe = {
  a: 1
}
export default App;
