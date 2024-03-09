<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";
  import { user$ } from "./store";
  import {
    getAuth,
    GoogleAuthProvider,
    signInWithCredential,
  } from "firebase/auth";
  import { onMount } from "svelte";
  import Loading from "./pages/Loading.svelte";
  import Mypage from "./pages/Mypage.svelte";
  // import { GoogleAuthProvider } from "firebase/auth";

  // const provider = new GoogleAuthProvider();
  // provider.addScope("https://www.googleapis.com/auth/contacts.readonly"); //읽기만 가능하도록

  // let login = false;

  let isLoading = true; //로딩 중이라는 메시지 보여줌
  // 토큰 정보를 바탕으로 로그인된 유저인지 판단하는 로직
  const checkLogin = async () => {
    const auth = getAuth();
    const token = localStorage.getItem("token");
    if (!token) return (isLoading = false);
    //토큰을 바탕으로 인증 진행하게 되고 유저정보 가져오게 되고 그걸 바탕으로 user 스토어에 업데이트
    const credential = GoogleAuthProvider.credential(null, token); // idtoken과 accesstoken 넣어줌 idtoken은 없어서 null로 지정
    const result = await signInWithCredential(auth, credential);
    const user = result.user;
    user$.set(user); //user store에 user 정보 업데이트
    isLoading = false;
  };

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "/my": Mypage,
    "*": NotFound,
  };
  //해당 화면이 렌더링 될 때마다 checklogin 진행되도록
  onMount(() => checkLogin());
</script>

{#if isLoading}
  <Loading />
  <!--로그인 상태가 아니면 로그인 페이지 보여주고 로그인이 되어 있으면 라우터로 이동해서 우리가 구현해 놓은 코드들을 보여줄 것-->
  <!--user$ 자체는 store의 wriable이기 때문에 이 안의 값을 가져오려면 $표시 꼭 붙여줘야 함 -->
{:else if !$user$}
  <Login />
{:else}
  <Router {routes} />
{/if}
