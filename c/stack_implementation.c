// GENERIC IMPLEMENTATION OF STACK IN C:


// stack.h

typedef struct {
	void *elems;
	int elemSize;
	int loglength;
	int alloclength;
	void (*freefn)(void*);
} Stack;

void StackNew(Stack *s, int elemSize);
void StackDispose(Stack *s);
void StackPush(Stack *s, void *elemAddr);
void StackPop(Stack *s, void *elemAddr);

// stack.c

void StackNew(Stack *s, int elemSize, void (*freefn)(void*))
{
	assert(s->elemSize > 0);
	s->elemSize = elemSize;
	s->loglength = 0;
	s->alloclength = 4;
	s->elems = malloc(4 * elemSize);
	s->freefn = freefn;
	assert(s->elems != NULL);
}

void StackDispose(Stack *s)
{
	if(s->freefn != NULL){
		for(int i = 0; i < s->loglength; i++){
			s->freefn((char*) s->elems + i * s->elemSize);
		}
	}
	free(s->elems);
}

void StackPush(Stack *s, void *elemAddr)
{
	if(s->loglength == s->alloclength)
		StackGrow(s);
	void *target = (char*)s->elems + s->loglength * s->elemSize;
	memcpy(target, elemAddr, s->elemSize);
	s->loglength++;
}

static void StackGrow(Stack *s)
{
	s->alloclength *= 2;
	s->elems = realloc(s->elems, s->alloclength * s->elemSize);
}

void StackPop(Stack *s, void *elemAddr)
{
	s->loglength--;
	void *source = (char *) s->elems + (s->loglength) * s->elemSize;
	memcpy(elemAddr, source, s->elemSize);
}

int main()
{
	const char *friends = {"Al", "Bob", "Carl"};
	Stack stringStack;
	StackNew(&stringStack, sizeof(char*), StringFree);
	for(int i = 0; i < 3; i++) {
		char *copy = strdup(friends[i]);
		StackPush(&stringStack, &copy);
	}
	char *name;
	for(int i = 0; i < 3; i++){
		StackPop(&stringStack, &name);
		printf("%s\n", name);
		free(name);
	}
	StackDispose(&stringStack);
}

//free function for string stack
void StringFree(void *elem)
{
	free(*(char **) elem);
}