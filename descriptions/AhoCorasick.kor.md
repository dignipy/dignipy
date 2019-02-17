# Aho-Corasick Trie (한글 버전 문서)

> 아호코라식 알고리즘은 One-to-Many 패턴 매칭 알고리즘입니다. 길이 n의 텍스트와 길이(m1, m2, ... + mk)의 k개의 패턴이 주어졌을 때, brute-force 방법은 n * (m1 + m2 + ... + mk)로 구현이 되지만, 아호코라식 알고리즘을 이용하면 패턴을 효율적으로 찾기 위한 Trie를 형성하는 데에 (m1 + m2 + ... + mk)이 걸리고, 이후에 길이 n의 텍스트가 주어지면 Trie 상의 노드를 n번만 순회함으로써 모든 패턴을 찾을 수 있습니다. KMP의 2차원(?) 구현 버전.

## 구현 설명 ([코드 바로가기](../Trie/ahocorasick.py))
1. Trie 형성
	- 여러 개의 패턴이 주어지면 기본 Trie를 생성합니다.
	- 단, 각 노드에는 몇 가지 정보가 추가됩니다. 
		- go 링크 (go function)
			- 자식 노드들을 저장합니다.
		- failure 링크 (failure function)
			- 패턴 매칭을 위해 Trie를 순회하다가 특정 노드에서 다음 노드로 넘어가다가 실패 했을 경우 이동해야할 노드를 가리킵니다.
		- output 링크
			- 기본적으로 패턴의 끝을 표시하는 용도지만, 다른 패턴의 부분 패턴과의 링크의 역할도 합니다.
				- 특정 노드가 패턴의 끝이면 자기 자신을 output 링크에 넣습니다.
		- pattern
			- 패턴의 끝인 노드는 패턴 자체도 같이 저장 해놓습니다. 효율적으로 패턴을 되찾기 위해 추가하였습니다. 더 나은 방법이 있는 경우 수정해주세요.

2. Failure link 구하기 
	- 각 노드를 BFS로 방문하면서 failure link를 찾습니다. 다음과 같은 방식으로 구합니다. 
	- current, next 두 개의 포인터 이용, (KMP 알고리즘과 같은 원리, prefix==suffix...)
		1. current가 root일 경우 next의 fail은 root입니다.
		2. 그 외의 경우엔 current를 임시 변수(dest)에 담아 두고 
			- (dest = dest.fail)을 dest의 go가 next의 key를 포함할 때 까지 반복 이동시킵니다. (until dest != root)
			- go에 next의 key를 포함하는 dest를 발견할 경우 next의 fail을 dest로 설정합니다.

3. 패턴 찾기
	- text의 char를 하나하나 훑음과 동시에 Trie를 순회하면서 패턴을 찾습니다.
		1. current = root 부터 시작합니다 
		2. current의 go에 next_char가 포함될 때까지, fail을 타고 current를 이동시킵니다.
		3. current의 go가 next_char를 포함할 경우 current를 해당 go[next_char] 노드로 설정합니다.
		4. current 노드의 output 링크를 확인해서 완성된 패턴을 수집합니다. (타고 타고 갈 수도)
		5. b-d 과정을 text의 다음 char를 가져오면서 반복합니다.


## 참고자료
- [알고리즘 설명 슬라이드](https://www.slideshare.net/ssuser81b91b/ahocorasick-algorithm): 가장 상세한 자료입니다. output 링크 초기화 하는 부분이 애매해서, 다른 방식으로 구현했고 잘 동작하는 것 같습니다.
- [알고리즘 설명 블로그](https://m.blog.naver.com/PostView.nhn?blogId=kks227&logNo=220992598966&proxyReferer=https%3A%2F%2Fwww.google.com%2F): 구현 부분을 참조하였습니다. search 해당하는 부분은 특정 문제에 한정시킨 버전으로 구현이 되어 새로 구현하였습니다.
