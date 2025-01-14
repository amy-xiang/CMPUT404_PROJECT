import React, { useContext, useState } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { Card, Icon, Image, Button, Label, Dropdown } from "semantic-ui-react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";
import "./PostComponent.scss";
import { Context } from "../../Context";
import { SERVER_HOST, MARKDOWN_TYPE, PLAINTEXT_TYPE } from "../../Constants";
import DeletePostModal from "./DeletePostModal";

const defaultProps = {
  title: "Test Title",
  description: "Some Description",
  content: "Some Content",
  contentType: "text/plain",
  author: { displayName: "John Appleseed", id: "1" },
  published: "2021-02-18T07:21:52.915800Z",
  visibility: "PUBLIC",
  id: "1",
};

const PostComponent = (props) => {
  const context = useContext(Context);
  let history = useHistory();
  const [deletePost, setDeletePost] = useState(false);
  const [shareLoading, setShareLoading] = useState(false);

  const passedValues = { ...defaultProps, ...props };
  const {
    id,
    title,
    description,
    content,
    contentType,
    author,
    published,
    visibility,
  } = passedValues;

  const renderContent = () => {
    if (!contentType) {
      return <p>No Content</p>;
    }

    if (contentType.includes("image")) {
      return <Image src={content} size="medium" />;
    } else if (contentType === MARKDOWN_TYPE) {
      return <ReactMarkdown plugins={[gfm]} children={content} />;
    } else if (contentType === PLAINTEXT_TYPE) {
      return <p>{content}</p>;
    }
  };

  const deletePostClick = () => {
    setDeletePost(!deletePost);
  };

  const sharePostFriends = async () => {
    setShareLoading(true);

    let postId = id.split("/");
    postId = postId.slice(-2)[0];

    const body = {
      from: context.user.id,
      share_to: "all",
    };

    try {
      const response = await axios.post(
        `${SERVER_HOST}/api/author/${context.user.id}/posts/${postId}/share/`,
        body,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      setShareLoading(false);
    } catch (error) {
      setShareLoading(false);
    }
  };

  const getPostHref = () => {
    if (!id) {
      return ``;
    }

    let postId = id.split("/");
    postId = postId.slice(-2)[0];

    const checkPath = window.location.pathname.split("/");

    if (
      checkPath.length >= 5 &&
      checkPath[2] === author.id &&
      checkPath[4] === postId
    ) {
      return ``;
    }

    return `/author/${author.id}/posts/${postId}`;
  };

  const handleSpecificPost = () => {
    history.push(getPostHref());
  };

  const handleEditPost = () => {
    let postId = id.split("/");
    postId = postId.slice(-2)[0];

    history.push(`/editpost/${postId}`);
  };

  return (
    <div className="custom-card">
      <DeletePostModal
        id={id}
        index={props.index}
        open={deletePost}
        setOpen={deletePostClick}
        handleDeletePost={props.handleDeletePost}
      />
      <Card fluid raised centered>
        <Card.Content>
          <Button.Group as="div" floated="right">
            <Dropdown
              icon={null}
              trigger={
                <>
                  <Button
                    basic
                    loading={shareLoading}
                    color="black"
                    icon="share alternate"
                  />
                </>
              }
            >
              <Dropdown.Menu>
                <Dropdown.Item onClick={sharePostFriends}>
                  Friends
                </Dropdown.Item>
                <Dropdown.Item>Author</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Button.Group>
          {context.user &&
            author.id === context.user.id &&
            visibility === "PUBLIC" && (
              <Button
                basic
                color="black"
                floated="right"
                icon="trash alternate"
                onClick={deletePostClick}
              />
            )}
          {context.user &&
            author.id === context.user.id &&
            visibility === "PUBLIC" && (
              <Button
                basic
                color="black"
                floated="right"
                icon="pencil"
                onClick={handleEditPost}
              />
            )}
          <Card.Header>{title}</Card.Header>
          <Card.Meta>
            <div>
              <Icon name="eye" />
              <span>
                {visibility &&
                  visibility.charAt(0) + visibility.substring(1).toLowerCase()}
              </span>
            </div>
            <div>
              <span className="date">
                Posted by{" "}
                <a href={author && `/author/${author.id}`}>
                  {author && (author.displayName || author.username)}
                </a>{" "}
                on {published}
              </span>
            </div>
          </Card.Meta>
          <Card.Description>{description}</Card.Description>
        </Card.Content>
        <Card.Content>
          <Card.Description>{renderContent()}</Card.Description>
        </Card.Content>
        <Card.Content extra>
          <Button as="div" labelPosition="right">
            <Button color="red">
              <Icon name="heart" />
              Like
            </Button>
            <Label as="a" basic color="red" pointing="left">
              0
            </Label>
          </Button>
          <Button as="div" labelPosition="left">
            <Button color="blue" floated="right" onClick={handleSpecificPost}>
              <Icon name="comments" />
              Comment
            </Button>
            <Label as="a" basic color="blue" pointing="left">
              0
            </Label>
          </Button>
        </Card.Content>
      </Card>
    </div>
  );
};

export default PostComponent;
