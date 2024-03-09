<script>
  import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
  import { user$ } from "../store";

  const provider = new GoogleAuthProvider();
  const auth = getAuth();
  //login-btn을 눌렀을 때만 팝업창이 뜨도록
  const loginWithGoolge = async () => {
    try {
      //signInWithPopup 결과를 기다림
      const result = await signInWithPopup(auth, provider);
      //팝업의 결과가 오면 그 결과에서 인증정보를 가져옴
      const credential = GoogleAuthProvider.credentialFromResult(result);
      //인증정보 안에 있는 토큰 가져옴
      const token = credential.accessToken;
      //인증정보 안에 있는 user 정보 가져옴
      const user = result.user;
      user$.set(user); //user정보 업데이트
      //로그인을 하면 받아온 토큰 정보를 로컬 스토리지에 저장
      localStorage.setItem("token", token);
    } catch (error) {
      console.error(error);
    }
  };
</script>

<div>
  <!-- {#if $user$}
    <div>{$user$?.displayName} 로그인됨</div>
    <!--displayName : 로그인된 유저가 누구인지 보여줌-->
  <!--$ 표시를 해줘야지 그 안에 있는 값을 보여줄 수 o
  {/if} -->

  <div>로그인하기</div>
  <button class="login-btn" on:click={loginWithGoolge}>
    <img
      class="google-img"
      src="https://w7.pngwing.com/pngs/869/485/png-transparent-google-logo-computer-icons-google-text-logo-google-logo-thumbnail.png"
      alt=""
    />
    <div>Google로 시작하기</div>
    <div />
  </button>
</div>

<style>
  .login-btn {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 200px;
    height: 50px;
    border: 1px solid gray;
    cursor: pointer;
    border-radius: 3px;
  }
  .google-img {
    width: 20px;
  }
</style>
