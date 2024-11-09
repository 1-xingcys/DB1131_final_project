import React, { useState } from 'react';

const DataTable = ({ column, table }) => {
  return (
    <table border="1">
      <thead>
        <tr>
          {column.map((col, index) => (
            <th key={index}>{col}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {table.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {row.map((cell, cellIndex) => (
              <td key={cellIndex}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};


function App() {
  const [message, setMessage] = useState('加载中...');
  
  const [sqlinput, setSqlInput] = useState('');  // 用户输入
  const [data, setData] = useState({ 'column' : [], 'table' : [] })

  // 加载初始数据
  React.useEffect(() => {
    console.log("backend url is")
    console.log(process.env.REACT_APP_BACKEND_URL)
    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/hello`)
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => console.error('错误:', error));
  }, []);

  // 处理表单提交
  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sqlinput })
    })
    .then(response => response.json())
    .then(responseData => setData(responseData))
    .catch(error => console.error('错误:', error));

    console.log(typeof data.column)
    console.log(data.column)
    console.log(typeof data.table)
    console.log(data.table)
  };

  const handleClear = () => {
    setData({ 'column' : [], 'table' : [] })
    setSqlInput('')
  }

  return (
    <div>
      <h1>DB Final Project Frontend / Backend Test</h1>
      <p>{message}</p>

      <form onSubmit={handleSearchSubmit}>
        <input
          type="text"
          value={sqlinput}
          onChange={(e) => setSqlInput(e.target.value)}
          placeholder="輸入 sql 指令"
        />
        <button type="submit">Enter</button>
      </form>

      {/* {data.column && <p>query success</p>}  顯示後端回應 */}

      {data.column && <DataTable column={data.column} table={data.table} />}

      <button type="clear" onClick={handleClear}>clear</button>
    </div>
  );
}

export default App;
