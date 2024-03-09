import { writable } from "svelte/store";

//user정보, writeable : svelte 스토어의 문법, 수정할 수 있는 값
export const user$ = writable(null); // 초기에는 null로 로그인이 안 되어있는 상태
//만약 로그인이 됐으면 로그인 상태를 여기에 저장시켜놓음
