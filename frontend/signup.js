const form = document.querySelector("#signup-form");

const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form); // id, password값 존재 {id : 'abc', password : '123'}
  //formData에서 password를 가져와서 sha256으로 감싸서 암호화
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password); //암호화한 값을 다시 password에 넣어줌

  const div = document.querySelector("#info");

  //password1과 password2가 같을 때만 서버에 요청보냄
  if (checkPassword()) {
    //서버로 보냄
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    //서버한테 요청하고 회원가입에 성공했다는 응답을 받았을 때만 성공했다는 메시지 출력
    if (data === "200") {
      alert("회원가입에 성공했습니다!");
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 같지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
