const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form); // id, password값 존재 {id : 'abc', password : '123'}
  //formData에서 password를 가져와서 sha256으로 감싸서 암호화
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password); //암호화한 값을 다시 password에 넣어줌

  //서버로 요청보냄
  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  // 서버에서 받은 응답을 가지고 json으로 바꿔줌
  const data = await res.json();
  const accessToken = data.access_token;
  //accessToken 받아와서 window.localStorage라는 곳에 새로운 아이템을 추가하는 setItem 호출
  window.localStorage.setItem("token", accessToken);
  alert("로그인 되었습니다!!");

  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmit);
