<script>
  import { getDatabase, ref, push } from "firebase/database";
  import {
    getStorage,
    ref as refImage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";
  import Nav from "../components/Nav.svelte";
  //firebase에서 push 가져옴
  let title;
  let price;
  let description;
  let place;
  let files;
  const db = getDatabase(); //db 정보 가져옴
  const storage = getStorage();

  function writeUserData(imgUrl) {
    //set(ref(db, "items/" + title)) items라는 곳에 title이라는 아이디를 추가
    push(ref(db, "items/"), {
      //items라는 곳에 값을 DB에 push
      title,
      price,
      description,
      place,
      insertAt: new Date().getTime(),
      imgUrl,
    });
    //alert은 안 쓰는 문법
    alert("글쓰기가 완료되었습니다.");
    window.location.hash = "/";
  }

  // 'file' comes from the Blob or File API
  // uploadBytes(storageRef, file).then((snapshot) => {
  //   console.log("Uploaded a blob or file!");
  // });
  //input 태그에 있는 데이터랑 연동
  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, name);
    await uploadBytes(imgRef, file);
    const url = await getDownloadURL(imgRef); //이미지의 정보 가져오기
    return url;
  };

  //uploadfile을 통해 이미지 업로드 하고 거기서 받아온 url을 바탕으로 userdata를 업데이트
  const handleSubmit = async () => {
    const url = await uploadFile(); //url 받아옴
    writeUserData(url);
  };
</script>

<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="image">이미지</label>
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <!--bind:value value 안에 있는 값을 js랑 연동시켜라 라는 의미-->
    <input type="text" id="title" name="title" bind:value={title} />
  </div>
  <div>
    <label for="price">가격</label>
    <input type="number" id="price" name="price" bind:value={price} />
  </div>
  <div>
    <label for="description">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="place">장소</label>
    <input type="text" id="place" name="place" bind:value={place} />
  </div>
  <div>
    <button class="write-button" type="submit">글쓰기 완료!</button>
  </div>
</form>
<Nav location="write" />

<style>
  .write-button {
    background-color: tomato;
    margin: 10px;
    border-radius: 10px;
    padding: 5px 12px 5px 12px;
    color: white;
    cursor: pointer;
  }
</style>
