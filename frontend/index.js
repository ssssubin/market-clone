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

//데이터들을 주는 함수
const renderData = (data) => {
  const main = document.querySelector("main");

  //데이터 불러옴, reverse() : 배열 안의 데이터들을 거꾸로 정렬
  data.forEach(async (obj) => {
    //obj : 데이터 값
    //CSS 파일을 className으로 미리 정해줘서 ClassName을 통해 css가 적용됨
    const div = document.createElement("div");
    div.className = "item-list";

    const imgDiv = document.createElement("div");
    imgDiv.className = "item-list__img";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob); //blob을 URL로 바꾸줌
    img.src = url; //blob을 url로 바꿔서 img에 삽입

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "item-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = "item-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "item-list__info-meta";
    InfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt); //insertAt: timestamp값 가지고 있음

    const InfoPriceDiv = document.createElement("div");
    InfoMetaDiv.className = "item-list__info-price";
    InfoPriceDiv.innerText = obj.price;

    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);
    imgDiv.appendChild(img);

    div.appendChild(imgDiv);
    div.appendChild(InfoDiv);
    main.appendChild(div);
  });
};

//서버로부터 데이터 받아옴
const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  renderData(data);
};

fetchList();
