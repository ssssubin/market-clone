<script>
  import { onMount } from "svelte";
  import { getDatabase, ref, onValue } from "firebase/database";
  import Nav from "../components/Nav.svelte";

  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  //반응형으로 화면을 구성하고 싶으면 $: 사용
  //items는 반응형 변수로 선언, 즉 이 값이 바뀌게 되면 밑에 header에서 items를 렌더링하고 있는 태그가 자동으로 화면을 업데이트 함
  $: items = [];

  const db = getDatabase();
  const itemsRef = ref(db, "items/");

  //svelte의 원리 중 하나가 javascipt 파일은 화면이 처음 뜰 때 한 번만 실행됨 그다음에는 데이터 가져오지 않음
  //그래서 화면이 보여질 때마다 실행되게 하고 싶으면 onMount 사용해서 화면이 렌더링될 때마다 밑에 있는 onvalue가 호출될 수 있도록 함
  onMount(() => {
    //글쓰기 페이지에서 리스트 받아오기(onValue 사용)
    //onValue 사용하면 itemsRef가 바뀔 때마다 snapshot이 새롭게 내려오고 data를 통해 items 업데이트 됨
    // 반응형 변수인 items가 업데이트 될 때마다 svelte가 자동으로 화면 업데이트 시켜줌
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val(); //object 형식
      //Object.values(data)=> data의 형식을 배열로 바꿔줌
      //items에 배열을 업데이트
      items = Object.values(data).reverse();
    });
  });

  //시간정보 함수
  const calcTime = (timestamp) => {
    // FormData가 세계시간으로 넘어오기 때문에 세계시간기준으로 맞춰주기 위해 9시간을 빼줘야함
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000; //9시간*60분*60초*1000(ms)
    const time = new Date(curTime - timestamp); //new Date()를 씌워주는 건 시간값으로 바꿔주기 위해
    const hour = time.getHours();
    const min = time.getMinutes();
    const sec = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (min > 0) return `${min}분 전`;
    else if (sec > 0) return `${sec}초 전`;
    else return "방금 전";
  };
</script>

<header>
  <!--block : info-bar Element : input Element 이름은 __로 구별, 어떤 element인지 --뒤에 설명까지 해주는 방법 => bem 명명법-->
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="assets/chart-bar.svg" alt="chart-bar" />
      <img src="assets/wifi.svg" alt="wifi" />
      <img src="assets/battery.svg" alt="battery" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <div class="menu-bar__location-icon">
        <img src="assets/arrow-down.svg" alt="arrow-down" />
      </div>
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="search" />
      <img src="assets/bar3.svg" alt="bar3" />
      <img src="assets/bell.svg" alt="bell" />
    </div>
  </div>
</header>
<!--main : 리스트-->
<main>
  <!--items라는 변수라는 배열에서 item을 가져옴 -->
  {#each items as item}
    <div class="item-list">
      <div class="item-list__img">
        <img alt={item.title} src={item.imgUrl} />
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list__info-meta">
          {item.place}
          {calcTime(item.insertAt)}
        </div>
        <div class="item-list__info-price">{item.price}</div>
        <div>{item.description}</div>
      </div>
    </div>
  {/each}
  <a class="write-btn" href="#/write">+ 글쓰기</a>
  <!--a태그는 하이퍼링크를 걸어줘서 특정 태그로 이동시켜주는 태그-->
</main>
<!--fotter : 내비게이션 바-->
<Nav location="home" />
<div class="media-info-msg">화면 사이즈를 줄여주세요.</div>

<style>
  .info-bar__time {
    color: blue;
  }
</style>
