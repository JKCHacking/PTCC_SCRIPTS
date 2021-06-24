void rotate(void *front, void *middle, void *end)
{
    int frontSize = (char*) middle - (char*) front;
    int backSize = (char*) end - (char*) middle;
    char buffer[frontSize];
    memcpy(buffer, front, fontSize);
    memmove(front, middle, backSize);
    memcpy((char*)end - frontSize, buffer, frontSize);
}